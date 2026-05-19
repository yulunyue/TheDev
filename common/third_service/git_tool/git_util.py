from common.tool.export import OsUtil, GC
from common.util.export import logger, List, File, Dict
import re
import fnmatch


class GitUtil(OsUtil):
    uri = "https://github.com/"

    def __init__(self, error_exit_flag=True, workdir: str = None):
        super().__init__("git", error_exit_flag)
        if workdir:
            self.set_env(workdir)

    owner = None

    def reset(self, commid_id):
        return self.run("reset", "--hard", commid_id)

    def clear(self):
        """
        fdx 全清理  fd清理跟踪的
        """
        return self.run("clean", "-fd")

    def set_repo_url(self, uri):
        self.repo_uri: str = uri
        owner, repo = self.repo_uri.split(self.uri).pop().split("/")
        return self.set_repo(owner, repo.split(".")[0])

    def get_repo_uri(self):
        return self.repo_uri

    def set_repo(self, owner, repo: str):
        self.owner = owner
        self.repo = repo
        self.set_local_dir(f"data/repo/{self.owner}/{self.repo}")
        return self

    def set_local_dir(self, f):
        if isinstance(f, str):
            f = File(f)
        self.local_dir = f
        self.set_env(f.path)
        return self

    def clone(self):
        if not self.local_dir.exists():
            self.local_dir.make_dir_if_not_exist()
            OsUtil("git").run(
                "clone",
                GC.git_proxy_prefix.get_value() + self.get_repo_uri(),
                self.local_dir.parent().path,
            )
        return self

    def get_pr(self, number):
        from common.model.git.pr_info import PrInfo

        return (
            PrInfo()
            .set_owner(self.owner)
            .set_repo(self.repo)
            .set_number(number)
            .set_local(self.local_dir)
        )

    def apply(self, path):
        self.run("apply", path)
        return self

    def commit(self):
        self.run("add", ".")
        self.run("commit", "-m", "xx")

    def diff(self):
        pass

    def check(self):
        self.run("checkout")

    def run(self, *args, env=None):
        return super().run(*args, env=env)

    def run_git_output(self, *args) -> str:
        """
        执行 git 命令并返回输出内容（不抛异常）
        """
        import subprocess

        cmd = ["git"] + list(args)
        try:
            result = subprocess.run(
                cmd,
                cwd=self.root_path,
                capture_output=True,
                text=True,
                timeout=60,
            )
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"git command failed: {cmd} -> {e}")
            return ""

    def get_current_branch(self) -> str:
        """
        获取当前分支名
        """
        return self.run_git_output("branch", "--show-current")

    def get_all_branches(self) -> List[str]:
        """
        获取所有本地分支名
        """
        output = self.run_git_output("branch", "--list")
        return [b.strip().lstrip("* ") for b in output.split("\n") if b.strip()]

    def is_clean(self) -> bool:
        """
        检查工作区是否干净（无未提交变更）
        """
        output = self.run_git_output("status", "--porcelain")
        return output == ""

    def get_diff_numstat(self, base: str, target: str) -> List[Dict]:
        """
        获取分支 diff 的数值统计

        返回: [{"file": str, "add": int, "del": int}, ...]
        """
        output = self.run_git_output("diff", f"{base}..{target}", "--numstat")
        result = []
        for line in output.split("\n"):
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    add = int(parts[0]) if parts[0] != "-" else 0
                    del_ = int(parts[1]) if parts[1] != "-" else 0
                    file = parts[2]
                    result.append({"file": file, "add": add, "del": del_})
        return result

    def get_diff_summary(self, base: str, target: str) -> Dict:
        """
        获取 diff 概要统计
        """
        files = self.get_diff_numstat(base, target)
        return {
            "total_files": len(files),
            "total_add": sum(f["add"] for f in files),
            "total_del": sum(f["del"] for f in files),
            "files": files,
        }

    def select_files_by_lines(
        self,
        file_stats: List[Dict],
        target_lines: int,
        threshold_ratio: float = 0.8,
    ) -> List[str]:
        """
        按行数阈值选择文件（小文件优先）

        策略：优先选择小文件，凑够目标行数
        threshold_ratio: 允许少量超出，如 0.8 表示达到 80% 即可
        """
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
        """
        按文件模式过滤（如 *.py, *.yml）
        """
        result = []
        for f in files:
            for pattern in patterns:
                if fnmatch.fnmatch(f["file"], pattern):
                    result.append(f)
                    break
        return result

    def generate_branch_name(self, base_name: str) -> str:
        """
        自动生成不重复的分支名（格式: {base}_part_N）
        """
        existing = self.get_all_branches()

        pattern = re.compile(r"_part_(\d+)$")
        max_n = 0
        for b in existing:
            if b.startswith(base_name):
                match = pattern.search(b)
                if match:
                    n = int(match.group(1))
                    max_n = max(max_n, n)

        return f"{base_name}_part_{max_n + 1}"

    def extract_branch_diff(
        self,
        base_branch: str,
        target_branch: str,
        extract_lines: int = 1800,
        new_branch_name: str = None,
        commit_message: str = None,
        file_patterns: List[str] = None,
        threshold_ratio: float = 0.8,
    ) -> Dict:
        """
        提取分支 diff 到新分支（checkout + copy 方式）

        流程：
        1. 从 base_branch checkout 新分支
        2. 从 target_branch 复制指定文件
        3. add + commit

        参数：
        - base_branch: 基础分支（如 origin/release）
        - target_branch: 目标分支（如 release_edkm）
        - extract_lines: 要提取的目标行数（默认 1800）
        - new_branch_name: 新分支名（自动生成则不填）
        - commit_message: 提交信息
        - file_patterns: 文件过滤（如 ["*.py"]）
        - threshold_ratio: 行数阈值比例（0.8 表示达到 80% 即可）

        返回：
        {
            "success": bool,
            "new_branch": str,
            "commit_files": List[str],
            "extracted_lines": int,
            "diff_summary": dict,
            "error": str
        }
        """
        try:
            if not self.is_clean():
                return {"success": False, "error": "工作区有未提交的变更，请先处理"}

            diff_files = self.get_diff_numstat(base_branch, target_branch)

            if not diff_files:
                return {"success": False, "error": f"分支 {base_branch} 和 {target_branch} 无差异"}

            if file_patterns:
                diff_files = self.filter_by_patterns(diff_files, file_patterns)

            selected_files = self.select_files_by_lines(
                diff_files, extract_lines, threshold_ratio
            )

            if not selected_files:
                return {"success": False, "error": "未找到符合条件的文件"}

            extracted_lines = sum(
                f["add"] for f in diff_files if f["file"] in selected_files
            )

            branch_base = target_branch.replace("origin/", "").replace("/", "_")
            new_branch = new_branch_name or self.generate_branch_name(branch_base)

            self.run_git_output("checkout", base_branch)
            self.run_git_output("checkout", "-b", new_branch)

            for file in selected_files:
                self.run_git_output("checkout", target_branch, "--", file)

            message = commit_message or f"阶段提交: 提取 {extracted_lines} 行变更"
            self.run("add", ".")
            self.run("commit", "-m", message)

            full_diff_summary = self.get_diff_summary(base_branch, target_branch)

            return {
                "success": True,
                "new_branch": new_branch,
                "commit_files": selected_files,
                "extracted_lines": extracted_lines,
                "total_files": len(diff_files),
                "total_add": sum(f["add"] for f in diff_files),
                "total_del": sum(f["del"] for f in diff_files),
                "full_diff_summary": full_diff_summary,
            }

        except Exception as e:
            logger.error(f"extract_branch_diff error: {e}")
            return {"success": False, "error": str(e)}

    def get_commits_between(self, base: str, target: str) -> List[Dict]:
        """
        获取分支间的提交列表
        """
        output = self.run_git_output("log", f"{base}..{target}", "--oneline")
        result = []
        for line in output.split("\n"):
            if line.strip():
                parts = line.split(" ", 1)
                if len(parts) == 2:
                    result.append({"commit": parts[0], "message": parts[1]})
        return result

    def get_file_content(self, branch: str, file: str) -> str:
        """
        从指定分支获取文件内容
        """
        return self.run_git_output("show", f"{branch}:{file}")

    def list_diff_files(self, base: str, target: str) -> List[str]:
        """
        仅列出变更文件名
        """
        output = self.run_git_output("diff", f"{base}..{target}", "--name-only")
        return [f.strip() for f in output.split("\n") if f.strip()]
