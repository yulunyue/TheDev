from common.util.export import ToolBase, logger, File
from common.third_service.git_tool.git_util import GitUtil
from common.third_util.api import Api


class ApiTool(ToolBase):
    def prepare(self, *args):
        Api.enable_globel_log()
        return super().prepare(*args)

    def git_query_pr(self):
        pr = GitUtil().set_repo("beeware", "briefcase").get_pr(2607)
        logger.info(pr.get_title())


if __name__ == "__main__":
    ApiTool().run()
