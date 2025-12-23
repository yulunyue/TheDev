from common.third_util.api import Api
from .pr_info import PrInfo


class GitHubApi(Api):
    def get_endpoint(self):
        return "https://api.github.com"

    def get_pr(self, pull_number):
        uri = f"/repos/{self.owner}/{self.repo}/pulls/{pull_number}"
        # r = self.github.get(uri)
        return PrInfo(files=self.github.get(f"{uri}/files?per_page=100"))
