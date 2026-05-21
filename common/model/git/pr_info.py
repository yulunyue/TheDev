from common.util.export import List, File, logger
from .file_change import FileChange
from .patch import Patch
from common.third_service.git_tool.git_api import GitHubApi


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