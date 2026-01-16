from common.util.export import ToolBase, logger, File
from common.third_service.git_tool.git_util import GitUtil


class ApiTool(ToolBase):
    def git_query_pr(self):
        g = GitUtil().set_owner("TobikoData").set_repo("sqlmesh")
        logger.map(
            t_1358=g.get_pr(1358).get_isure(),
            t_2282=g.get_pr(2282).get_isure(),
        )


if __name__ == "__main__":
    ApiTool().run()
