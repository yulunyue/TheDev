from common.tool.export import OsUtil, GC
from common.util.export import logger, List, File

from common.model.git.patch import Patch
from common.model.git.pr_info import PrInfo


class GitUtil(OsUtil):
    uri = "https://github.com/"

    def __init__(self, error_exit_flag=True):
        super().__init__("git", error_exit_flag)

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
        self.run("add .")
        self.run("commit", "-m", "xx")

    def diff(self):
        pass

    def check(self):
        self.run("checkout")

    def run(self, *args, env=None):
        return super().run(*args, env=env)
