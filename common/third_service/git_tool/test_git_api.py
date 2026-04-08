from common.util.export import TestBase
from common.third_service.git_tool.git_util import GitUtil


class TestGitApi(TestBase):
    def test_pr(self):
        GitUtil().set_repo("beeware", "briefcase")
