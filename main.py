import sys
from common.util.tool import SYS_KW, THE_DEV_LOGGER_PREFIX

SYS_KW[THE_DEV_LOGGER_PREFIX] = sys.argv[1] if len(sys.argv) > 1 else "dev"
from common.third_util.http import run, TornadaWebSocketConnectHandler
from common.util.export import logger, IO_MANAGE, Module
from common.tool.export import HttpConfig


def start():
    env = sys.argv[1] if len(sys.argv) > 1 else "dev"
    TornadaWebSocketConnectHandler.handler_msg = IO_MANAGE.handler_msg
    HttpConfig.set_resource("config/setting/http.json")
    conf = HttpConfig.get(env)
    plugins = conf.plugins.get_value()
    for p in plugins:
        obj = Module().load_module_object(p["entry"])
        obj(*p.get("args", []), **p.get("kwargs", {}))
        logger.info(f"plugin started: {p['name']}")
    port = SYS_KW.get("port", conf.port.get_value())
    run(conf.py_modules.get_value(), port=port)


if __name__ == "__main__":
    start()
