from common.tool.toolbase import ToolBase
from common.util.export import logger, File
from common.third_service.git_tool.git_util import GitUtil
from common.third_util.io.api import Api
from common.third_util.io.http_util import requests


STATUS_TITLE_MAP = {
    "running": "执行中",
    "completed": "执行完成",
    "failed": "执行失败",
    "blocked": "执行阻塞",
}


class ApiTool(ToolBase):
    def prepare(self, *args):
        Api.enable_globel_log()
        return super().prepare(*args)


if __name__ == "__main__":
    ApiTool().run()
