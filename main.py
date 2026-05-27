import sys
from common.util.tool import SYS_KW, THE_DEV_LOGGER_PREFIX

SYS_KW[THE_DEV_LOGGER_PREFIX] = sys.argv[1] if len(sys.argv) > 1 else "dev"
from common.third_util.http import run, TornadaWebSocketConnectHandler
from common.util.export import File, logger, IO_MANAGE, Module


def start():
    env = sys.argv[1] if len(sys.argv) > 1 else "dev"
    TornadaWebSocketConnectHandler.handler_msg = IO_MANAGE.handler_msg
    HTTP_CONF_FILE = File(f"config/setting/{env}.json").write_if_not_exists(
        dict(
            py_modules=[
                dict(
                    path="./",
                    modules={
                        "/app/agent": "app.tool.agent::Agent",
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

    logger.info(HTTP_CONF_FILE)
    conf = HTTP_CONF_FILE.read_file()
    plugins = conf.get("plugins", [])
    for p in plugins:
        obj = Module().load_module_object(p["module"])
        method = getattr(obj, p["method"])
        method(*p.get("args", []), **p.get("kwargs", {}))
        logger.info(f"plugin started: {p['name']}")
    port = SYS_KW.get("port", conf["port"])
    run(conf["py_modules"], port=port)


if __name__ == "__main__":
    start()
