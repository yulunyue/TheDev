from common.tool.export import OsUtil, GC
from common.util.export import logger, List, File, Dict, re, json, sys
import fnmatch


class GitUtil(OsUtil):

    def __init__(self, error_exit_flag=True, workdir: str = None):
        super().__init__("git", error_exit_flag)
        if workdir:
            self.set_env(workdir)

    def run_git_output(self, *args) -> str:
        return self.popen_output(*args, timeout=60)

    def reset(self, commit_id):
        return self.run("reset", "--hard", commit_id)

    def clear(self):
        return self.run("clean", "-fd")

    def apply(self, path):
        self.run("apply", path)
        return self

    def commit(self, message="auto commit"):
        self.run("add", ".")
        self.run("commit", "-m", message)

    def get_current_branch(self) -> str:
        return self.run_git_output("branch", "--show-current")

    def get_all_branches(self) -> List[str]:
        output = self.run_git_output("branch", "--list")
        return [b.strip().lstrip("* ") for b in output.split("\n") if b.strip()]

    def generate_branch_name(self, base_name: str) -> str:
        existing = self.get_all_branches()
        pattern = re.compile(r"_part_(\d+)$")
        max_n = 0
        for b in existing:
            if b.startswith(base_name):
                match = pattern.search(b)
                if match:
                    max_n = max(max_n, int(match.group(1)))
        return f"{base_name}_part_{max_n + 1}"

    def get_commit_hash(self, ref: str = "HEAD") -> str:
        return self.run_git_output("rev-parse", "--short", ref)

    def get_commits_between(self, base: str, target: str) -> List[Dict]:
        output = self.run_git_output("log", f"{base}..{target}", "--oneline")
        result = []
        for line in output.split("\n"):
            if line.strip():
                parts = line.split(" ", 1)
                if len(parts) == 2:
                    result.append({"commit": parts[0], "message": parts[1]})
        return result

    def is_clean(self) -> bool:
        return self.run_git_output("status", "--porcelain") == ""

    def get_diff_numstat(self, base: str, target: str) -> List[Dict]:
        output = self.run_git_output("diff", f"{base}..{target}", "--numstat")
        result = []
        for line in output.split("\n"):
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    add = int(parts[0]) if parts[0] != "-" else 0
                    del_ = int(parts[1]) if parts[1] != "-" else 0
                    result.append({"file": parts[2], "add": add, "del": del_})
        return result

    def get_diff_summary(self, base: str, target: str) -> Dict:
        files = self.get_diff_numstat(base, target)
        return {
            "total_files": len(files),
            "total_add": sum(f["add"] for f in files),
            "total_del": sum(f["del"] for f in files),
            "files": files,
        }

    def list_diff_files(self, base: str, target: str) -> List[str]:
        output = self.run_git_output("diff", f"{base}..{target}", "--name-only")
        return [f.strip() for f in output.split("\n") if f.strip()]

    def get_deleted_files(self, base: str, target: str) -> List[str]:
        output = self.run_git_output(
            "diff", "--name-only", "--diff-filter=D", f"{base}..{target}"
        )
        return [f.strip() for f in output.split("\n") if f.strip()]

    def get_added_files(self, base: str, target: str) -> List[str]:
        output = self.run_git_output(
            "diff", "--name-only", "--diff-filter=A", f"{base}..{target}"
        )
        return [f.strip() for f in output.split("\n") if f.strip()]

    def get_modified_files(self, base: str, target: str) -> List[str]:
        output = self.run_git_output(
            "diff", "--name-only", "--diff-filter=M", f"{base}..{target}"
        )
        return [f.strip() for f in output.split("\n") if f.strip()]

    def get_file_content(self, branch: str, file: str) -> str:
        return self.run_git_output("show", f"{branch}:{file}")

    def select_files_by_lines(
        self,
        file_stats: List[Dict],
        target_lines: int,
        threshold_ratio: float = 0.8,
    ) -> List[str]:
        sorted_files = sorted(file_stats, key=lambda x: x["add"])
        selected = []
        total_lines = 0
        for f in sorted_files:
            file_lines = f["add"]
            if file_lines == 0:
                continue
            if total_lines + file_lines <= target_lines:
                selected.append(f["file"])
                total_lines += file_lines
            elif total_lines < target_lines * threshold_ratio:
                selected.append(f["file"])
                total_lines += file_lines
                break
            else:
                break
        return selected

    def filter_by_patterns(self, files: List[Dict], patterns: List[str]) -> List[Dict]:
        result = []
        for f in files:
            for pattern in patterns:
                if fnmatch.fnmatch(f["file"], pattern):
                    result.append(f)
                    break
        return result

    def push_branch(self, branch: str, remote: str = "origin") -> Dict:
        old_flag = self.error_exit_flag
        self.error_exit_flag = False
        proc = self.popen("push", remote, branch)
        try:
            stdout, stderr = proc.communicate(timeout=60)
            if proc.returncode == 0:
                return {"success": True, "remote": remote, "branch": branch}
            else:
                return {"success": False, "error": stderr.strip()}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            self.error_exit_flag = old_flag

    def extract_diff(
        self,
        base_branch: str,
        target_branch: str,
        commit_msg: str,
        filter_type: str = "modified",
        push: bool = False,
    ) -> Dict:
        try:
            if not self.is_clean():
                return {"success": False, "error": "工作区有未提交的变更"}

            if filter_type == "deleted":
                files = self.get_deleted_files(base_branch, target_branch)
            elif filter_type == "added":
                files = self.get_added_files(base_branch, target_branch)
            else:
                files = self.get_modified_files(base_branch, target_branch)

            if not files:
                return {"success": False, "error": f"无 {filter_type} 文件"}

            branch_base = target_branch.replace("origin/", "").replace("/", "_")
            suffix = "_del" if filter_type == "deleted" else "_part"
            new_branch = self.generate_branch_name(branch_base + suffix)

            self.run_git_output("checkout", base_branch)
            self.run_git_output("checkout", "-b", new_branch)

            if filter_type == "deleted":
                for file in files:
                    self.run_git_output("rm", "--", file)
            else:
                for file in files:
                    self.run_git_output("checkout", target_branch, "--", file)

            self.commit(commit_msg)
            commit_hash = self.get_commit_hash()

            if push:
                push_result = self.push_branch(new_branch)
                if not push_result["success"]:
                    return {
                        "success": False,
                        "error": f"push 失败: {push_result['error']}",
                        "new_branch": new_branch,
                        "commit_hash": commit_hash,
                        "files": files,
                    }

            return {
                "success": True,
                "new_branch": new_branch,
                "files": files,
                "commit_hash": commit_hash,
            }

        except Exception as e:
            logger.error(f"extract_diff error: {e}")
            return {"success": False, "error": str(e)}

    def get_review_suggestion(
        self,
        opencode_config: str,
        base_branch: str,
        target_branch: str,
        suggestion_count: int = 5,
    ) -> Dict:
        from common.third_util.llm.export import OpencodeClient

        client = OpencodeClient(opencode_config)
        llm_cwd = client.config.cwd.get_value()
        if not llm_cwd:
            return {
                "ok": False,
                "error": f"工作目录不一致: {opencode_config}, llm={llm_cwd}",
            }
        self.set_env(llm_cwd)
        self.run_git_output("fetch", "origin")
        diff = self.run_git_output(
            "diff", "--unified=0", f"origin/{base_branch}..origin/{target_branch}"
        )
        if not diff.strip():
            return {"ok": False, "error": "无差异内容"}

        prompt = f"""分析以下 git diff，提供 {suggestion_count} 个代码检视建议。
仅返回 JSON 格式：
{{"suggestions": [{{"file": "文件路径", "line": 行号, "severity": "high/medium/low", "type": "问题类型", "message": "问题描述", "suggestion": "改进建议"}}], "summary": "整体评价"}}

diff:
{diff[:8000]}"""

        client.start_server()
        response = client.do_prompt(prompt)

        if response.startswith("```json"):
            response = (
                response.strip().replace("```json", "").replace("```", "").strip()
            )
        elif response.startswith("```"):
            response = response.strip().replace("```", "").strip()

        try:
            result = json.loads(response)
            result.update(
                {"ok": True, "base_branch": base_branch, "target_branch": target_branch}
            )
            return result
        except json.JSONDecodeError:
            return {"ok": False, "error": "响应解析失败", "raw": response[:200]}
