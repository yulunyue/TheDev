from common.util.export import ToolBase, logger, File
from common.third_service.git_tool.git_util import GitUtil


class ApiTool(ToolBase):
    def git_query_pr(self):
        g = GitUtil().set_repo("TobikoData", "sqlmesh")
        logger.map(
            t_1358=g.get_pr(1358).get_title(),
            t_2282=g.get_pr(2282).get_title(),
            t_2486=g.get_pr(2486).get_title(),
        )


if __name__ == "__main__":
    ApiTool().run()
