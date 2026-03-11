from common.util.export import ToolBase, logger, File
from common.third_service.git_tool.git_util import GitUtil
from common.third_util.io.api import Api


class ApiTool(ToolBase):
    def prepare(self, *args):
        Api.enable_globel_log()
        return super().prepare(*args)


if __name__ == "__main__":
    ApiTool().run()
