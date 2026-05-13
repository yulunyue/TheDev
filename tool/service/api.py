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

    def qt_status(self, key: str, status: str, user: str):
        """
        发送 opencode session 状态消息
        
        :param key: session ID
        :param status: 状态英文
        :param user: 用户名
        """
        title = STATUS_TITLE_MAP.get(status, status)
        value = {
            "key": key,
            "title": title,
            "status": status,
            "user": user,
        }
        requests.post(
            "http://localhost:9999/app/manage/send_msg",
            json={"topic": "TOPIC_MSG_QT", "value": value},
        )
        return value


if __name__ == "__main__":
    ApiTool().run()
