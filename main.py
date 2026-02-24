import sys
import os
from common.util.tool import SYS_KW, THE_DEV_LOGER_PREFIX

SYS_KW[THE_DEV_LOGER_PREFIX] = "main"
from common.third_util.http import run
from common.util.export import File, logger
from common.tool.export import ToolBase


def start():
    HTTP_CONF_FiLE = File(f"config/setting/{sys.argv[1]}.json")
    logger.info(HTTP_CONF_FiLE)
    conf = HTTP_CONF_FiLE.read_file()
    run(conf["py_modules"], port=conf.get("port", 9999))


if __name__ == "__main__":
    start()
