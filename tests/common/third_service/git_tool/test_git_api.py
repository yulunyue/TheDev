from common.util.export import TestBase
from common.third_service.git_tool.git_util import GitUtil


class TestGitApi(TestBase):
    def test_pr(self):
        g = GitUtil().set_repo("beeware", "briefcase")
        self.expect(g.get_pr(2607).get_link_isures()[0]["number"], 2525)
        g = GitUtil().set_repo("TobikoData", "sqlmesh")
        self.expect(g.get_pr(1358).get_link_isures(), [])
        self.expect(g.get_pr(2282).get_link_isures()[0]["number"], 2276)
