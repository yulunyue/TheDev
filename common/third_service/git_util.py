from common.tool.export import OsUtil, GC
from common.util.export import logger, List
from common.service.api import Api


class GitHubApi(Api):
    def get_endpoint(self):
        return "https://api.github.com"


class FileChange:
    def __init__(self, filename, **kw):
        self.filename: str = filename

    def to_json(self):
        return {"filename": self.filename}


class PrInfo:
    def __init__(self, files: List[dict] = None, **kwargs):
        self.files = [FileChange(**d) for d in files or []]


class GitUtil(OsUtil):
    def __init__(self, error_exit_flag=True):
        super().__init__("git", error_exit_flag)
        self.github = GitHubApi(log_enable=True)

    def clone(self, repo, local_dir):
        return self.run("clone", GC.git_proxy_prefix.get_value() + repo, local_dir)

    def set_owner(self, owner):
        self.owner = owner
        return self

    def set_repo(self, repo):
        self.repo = repo
        return self

    def get_pr_info(self, pull_number):
        uri = f"/repos/{self.owner}/{self.repo}/pulls/{pull_number}"
        # r = self.github.get(uri)
        return PrInfo(files=self.github.get(f"{uri}/files?per_page=100"))
