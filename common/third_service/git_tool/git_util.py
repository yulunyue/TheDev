from common.tool.export import OsUtil, GC
from common.util.export import List


class GitUtil(OsUtil):

    def __init__(self, error_exit_flag=True, workdir: str = None):
        super().__init__("git", error_exit_flag)
        if workdir:
            self.set_env(workdir)

    def run_git_output(self, *args, **kw) -> str:
        return self.popen_output(*args, timeout=60, **kw)

    def git_fetch(self, remote="origin") -> str:
        return self.run_git_output("fetch", remote)

    def git_reset(self, commit_id) -> str:
        return self.run_git_output("reset", "--hard", commit_id)

    def git_clean(self) -> str:
        return self.run_git_output("clean", "-fd")

    def git_apply(self, path) -> str:
        return self.run_git_output("apply", path)

    def git_add(self, path=".") -> str:
        return self.run_git_output("add", path)

    def git_commit(self, message) -> str:
        return self.run_git_output("commit", "-m", message)

    def git_push(self, remote, branch) -> str:
        return self.run_git_output("push", remote, branch)

    def git_checkout(self, *args) -> str:
        return self.run_git_output("checkout", *args)

    def git_branch(self, *args) -> str:
        return self.run_git_output("branch", *args)

    def git_rev_parse(self, *args) -> str:
        return self.run_git_output("rev-parse", *args)

    def git_log(self, *args) -> str:
        return self.run_git_output("log", *args)

    def git_status(self, *args) -> str:
        return self.run_git_output("status", *args)

    def git_diff(self, *args) -> str:
        cmd = self.get_cmd(["diff"] + list(args), {})
        _, stdout, _ = self.check_output(cmd, capture_output=True)
        return stdout

    def git_show(self, ref) -> str:
        cmd = self.get_cmd(["show", ref], {})
        _, stdout, _ = self.check_output(cmd, capture_output=True)
        return stdout

    def git_rm(self, file) -> str:
        return self.run_git_output("rm", "--", file)

    def get_current_branch(self) -> str:
        return self.git_branch("--show-current")

    def get_all_branches(self) -> List[str]:
        output = self.git_branch("--list")
        return [b.strip().lstrip("* ") for b in output.split("\n") if b.strip()]

    def get_commit_hash(self, ref="HEAD") -> str:
        return self.git_rev_parse("--short", ref)

    def is_clean(self) -> bool:
        return self.git_status("--porcelain") == ""

    def get_file_content(self, branch: str, file: str) -> str:
        return self.git_show(f"{branch}:{file}")

    def git_clone(self, url, dest=None, depth=None):
        http_proxy = GC.http_proxy.get_value()
        env = {"GIT_SSL_NO_VERIFY": "1"}
        if http_proxy:
            env["HTTP_PROXY"] = str(http_proxy)
            env["HTTPS_PROXY"] = str(http_proxy)

        args = ["clone", url]
        if dest:
            args.append(dest)
        if depth:
            args.extend(["--depth", str(depth)])

        return self.run(*args, env=env or None)