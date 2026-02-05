import sys
import os
from common.util.tool import SYS_KW, THE_DEV_LOGER_PREFIX

SYS_KW[THE_DEV_LOGER_PREFIX] = "main"
from common.third_util.http import run
from common.util.export import File, logger
from app.tool.task import start_task

if __name__ == "__main__":
    HTTP_CONF_FiLE = File(f"config/setting/{sys.argv[1]}.json")
    logger.info(HTTP_CONF_FiLE)
    conf = HTTP_CONF_FiLE.read_file()
    start_task()
    run(conf["py_modules"], port=conf["port"])
