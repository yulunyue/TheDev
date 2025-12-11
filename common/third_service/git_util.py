from common.tool.export import OsUtil, GC


class GitUtil(OsUtil):
    def __init__(self, error_exit_flag=True):
        super().__init__("git", error_exit_flag)

    def clone(self, repo, local_dir):
        return self.run("clone", GC.git_proxy_prefix.get_value() + repo, local_dir)
