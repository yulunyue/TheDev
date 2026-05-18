from common.util.export import List, File, logger
from .file_change import FileChange
from .patch import Patch
from common.third_service.git_tool.git_api import GitHubApi
from common.third_util.llm.opencode import OpencodeClient
import json


class PrInfo:
    title = None

    def set_owner(self, owner):
        self.owner = owner
        return self

    def load(self, title="", **kw):
        self.title = title
        return self

    def get_title(self):
        self.get_config()
        return self.title

    link_isure = None

    def get_link_isures(self):
        if self.link_isure is None:
            self.link_isure = (
                GitHubApi().load(self.owner, self.repo).get_pr_link_isure(self.number)
            )
        return self.link_isure

    def set_repo(self, repo):
        self.repo = repo
        return self

    def set_local(self, local):
        self.local: File = local
        return self

    def set_number(self, number):
        self.number = number
        return self

    def __init__(self, files: List[dict] = None, **kwargs):
        self.files = [FileChange(**d) for d in files or []]

    def get_patch(self, f: File):

        return Patch().set_file(f).set_pr(self)

    config = None

    def get_config(self):
        if self.config is None:
            self.config = (
                GitHubApi().load(self.owner, self.repo).get_pr_info(self.number)
            )
            self.load(**self.config["files"])
        return self.config

    def to_json(self):
        return dict(title=self.title)

    _diff_content = None

    def get_diff_content(self) -> str:
        """
        获取 PR 的完整 diff 内容
        """
        if self._diff_content is None:
            self._diff_content = GitHubApi().load(
                self.owner, self.repo
            ).get_pr_diff(self.number)
        return self._diff_content

    _issue_info = None

    def get_issue_content(self) -> dict:
        """
        获取关联 Issue 的内容（如果存在）
        返回：Issue 信息字典，若无关联 Issue 返回 None
        """
        if self._issue_info is None:
            issues = self.get_link_isures()
            if issues and len(issues) > 0:
                issue = issues[0]
                issue_number = issue.get("number")
                if issue_number:
                    api = GitHubApi().load(self.owner, self.repo)
                    issue_detail = api.get_issue(issue_number)
                    self._issue_info = {
                        "number": issue_number,
                        "title": issue_detail.get("title", ""),
                        "body": issue_detail.get("body", ""),
                        "url": issue.get("url", ""),
                    }
        return self._issue_info

    _session_id = None

    def _build_review_prompt(self, diff_content: str, issue_info: dict = None) -> str:
        """
        构建 LLM 分析 prompt
        """
        issue_section = ""
        if issue_info:
            issue_section = f"""
## 关联 Issue
- 编号：#{issue_info["number"]}
- 标题：{issue_info["title"]}
- 内容：{issue_info["body"][:500] if issue_info["body"] else "无描述"}
- URL：{issue_info["url"]}
"""
        prompt = f"""
请分析以下 GitHub Pull Request 的代码变更，给出结构化的代码整改建议。

## PR 信息
- 标题：{self.title or self.get_title()}
- 编号：#{self.number}
- 仓库：{self.owner}/{self.repo}
{issue_section}

## 代码变更 (diff)
```
{diff_content[:8000]}
```

请返回 JSON 格式的分析结果，格式如下：
```json
{{"suggestions": [{{"file": "文件路径", "line_range": [起始行号, 结束行号], "severity": "high|medium|low", "type": "bug|style|performance|security|logic|documentation", "message": "问题描述", "suggestion": "整改建议"}}], "summary": "总体评价和总结"}}
```

注意：
1. 只返回 JSON，不要有其他文字
2. 如果代码质量良好，suggestions 可以为空数组
3. severity 根据问题严重程度判断：bug/security 为 high，logic/performance 为 medium，style/documentation 为 low
4. 如果有关联 Issue，请评估代码变更是否解决了 Issue 描述的问题
"""
        return prompt

    def get_review_suggestion(self) -> dict:
        """
        获取代码整改意见

        返回结构：
        {
            "pr_title": str,
            "pr_number": int,
            "issue_info": dict | None,
            "files": [{"filename": str, "change_type": str}],
            "suggestions": [{...}],
            "summary": str,
            "raw_response": str
        }
        """
        try:
            diff_content = self.get_diff_content()
            issue_info = self.get_issue_content()

            prompt = self._build_review_prompt(diff_content, issue_info)

            client = OpencodeClient()
            if self._session_id is None:
                session = client.create_session()
                if session:
                    self._session_id = session.id
                else:
                    return {"error": "Failed to create session"}

            response = client.execute_task(self._session_id, prompt)

            suggestions = []
            summary = ""
            raw_response = response

            if response and not response.startswith("execute_task error"):
                try:
                    json_str = response
                    if "```json" in json_str:
                        json_str = json_str.split("```json")[1].split("```")[0]
                    elif "```" in json_str:
                        json_str = json_str.split("```")[1].split("```")[0]
                    json_str = json_str.strip()
                    result = json.loads(json_str)
                    suggestions = result.get("suggestions", [])
                    summary = result.get("summary", "")
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON parse error: {e}")
                    suggestions = []
                    summary = response

            files = []
            for line in diff_content.split("\n"):
                if line.startswith("diff --git "):
                    filename = line.split(" ")[-1][2:]
                    files.append({"filename": filename, "change_type": "modified"})

            return {
                "pr_title": self.title or self.get_title(),
                "pr_number": self.number,
                "issue_info": issue_info,
                "files": files,
                "suggestions": suggestions,
                "summary": summary,
                "raw_response": raw_response,
            }
        except Exception as e:
            logger.error(f"get_review_suggestion error: {e}")
            return {"error": str(e)}