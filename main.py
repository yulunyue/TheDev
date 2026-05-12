import sys
import os
from common.util.tool import SYS_KW, THE_DEV_LOGER_PREFIX

SYS_KW[THE_DEV_LOGER_PREFIX] = sys.argv[1] if len(sys.argv) > 1 else "dev"
from common.third_util.http import run, TornadaWebSocketConnectHandler
from common.util.export import File, logger, IO_MANAGE
from common.tool.export import TASK_MANAGE, ProcessLock


def start():
    env = sys.argv[1] if len(sys.argv) > 1 else "dev"
    lock = ProcessLock(env)
    lock.start_unique()
    lock.set_pid(os.getpid())

    TornadaWebSocketConnectHandler.hander_msg = IO_MANAGE.hander_msg
    HTTP_CONF_FiLE = File(f"config/setting/{env}.json").write_if_not_exists(
        dict(
            py_modules=[
                dict(
                    path="./",
                    modules={
                        "/app/manage": "app.tool.manage::Manage",
                        "/app/user": "app.tool.user::User",
                        "/app/todo": "app.tool.todo::Todo",
                        "/app/api": "app.tool.api::ApiGlobal",
                    },
                )
            ],
            port=9999,
        )
    )

    logger.info(HTTP_CONF_FiLE)
    conf = HTTP_CONF_FiLE.read_file()
    TASK_MANAGE.set_resource("config/setting/task.json").start()
    port = SYS_KW.get("port", conf["port"])
    run(conf["py_modules"], port=port)


if __name__ == "__main__":
    start()
