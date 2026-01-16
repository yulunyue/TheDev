from common.third_util.api import Api


class GitHubApi(Api):
    def load(self, owner, repo):
        self.owner = owner
        self.repo = repo
        return self

    def get_endpoint(self):
        return "https://api.github.com"

    def get_pr(self, pull_number, is_file=False):
        uri = f"/repos/{self.owner}/{self.repo}/pulls/{pull_number}"
        if is_file:
            uri += "/files?per_page=100"
        return dict(files=self.get(uri))

    def get_pr_info(self, pull_number):
        return self.get_pr(pull_number)
