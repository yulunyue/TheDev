from common.tool.export import OsUtil, GC
from common.util.export import logger, List, File

from .patch import Patch
from .pr_info import PrInfo


class GitUtil(OsUtil):
    def __init__(self, error_exit_flag=True):
        super().__init__("git", error_exit_flag)

    owner = None

    def set_owner(self, owner):
        self.owner = owner
        return self

    def reset(self, commid_id):
        return self.run("reset", "--hard", commid_id)

    def clear(self):
        return self.run("clean", "-fdx")

    def set_repo(self, repo):
        self.repo: File = repo
        return self

    def set_local_dir(self, f):
        if isinstance(f, str):
            f = File(f)
        self.local_dir = f
        self.set_env(f.path)
        return self

    def clone(self):
        if not self.local_dir.exists():
            self.run(
                "clone",
                GC.git_proxy_prefix.get_value() + self.repo,
                self.local_dir.path,
            )
        return self

    def get_pr(self, number):
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

    def run(self, *args, capture_output=False, env=None):
        return super().run(*args, capture_output=capture_output, env=env)
