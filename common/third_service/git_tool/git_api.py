from common.third_util.api import Api


class GitHubApi(Api):
    def load(self, owner, repo):
        self.owner = owner
        self.repo = repo
        return self

    def get_endpoint(self):
        return "https://api.github.com"

    def get_pr(self, pull_number, path=""):
        uri = f"/repos/{self.owner}/{self.repo}/pulls/{pull_number}"
        if path:
            uri += path

        return dict(files=self.get(uri))

    def get_pr_info(self, pull_number):
        return self.get_pr(pull_number)

    def get_pr_files(self, pull_number):
        return self.get_pr(pull_number, "/files?per_page=100")

    def get_pr_link_isure(self, pull_numer):
        return self.get_pr(pull_numer, "/linked_issues")
