from common.third_util.io.api import Api
from common.tool.export import GC


class GitHubApi(Api):
    def load(self, owner, repo):
        self.owner = owner
        self.repo = repo
        return self

    def get_pr(self, pull_number, path=""):
        uri = f"/repos/{self.owner}/{self.repo}/pulls/{pull_number}"
        if path:
            uri += path

        return dict(files=self.get(uri))

    def get_pr_info(self, pull_number):
        return self.get_pr(pull_number)

    def get_pr_files(self, pull_number):
        return self.get_pr(pull_number, "/files?per_page=100")

    def graphql(self, query):
        headers = {"Authorization": f"Bearer {self.get_config('Authorization')}"}
        data = self.post("graphql", dict(query=query), headers=headers)
        return data

    def get_pr_link_isure(self, pull_numer):
        query = """
        query {
        repository(owner: "%s", name: "%s") {
            pullRequest(number: %s) {
            closingIssuesReferences(first: 10) {
                totalCount
                nodes {
                number
                url
                }
            }
            }
        }
        }
        """ % (
            self.owner,
            self.repo,
            pull_numer,
        )

        data = self.graphql(query)
        if "errors" in data:
            return None
        return data["data"]["repository"]["pullRequest"]["closingIssuesReferences"][
            "nodes"
        ]

    def get_pr_diff(self, pull_number) -> str:
        """
        获取 PR 的 diff 内容（patch 格式）
        """
        headers = {
            "Accept": "application/vnd.github.v3.patch",
            "Authorization": f"Bearer {GC.github_token.get_value()}",
        }
        res, content = self.http(
            "GET",
            f"/repos/{self.owner}/{self.repo}/pulls/{pull_number}",
            headers=headers,
        )
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        return content

    def get_issue(self, issue_number) -> dict:
        """
        获取 Issue 详情
        """
        return self.get(f"/repos/{self.owner}/{self.repo}/issues/{issue_number}")
