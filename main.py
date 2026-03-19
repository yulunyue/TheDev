import sys
import os
from common.util.tool import SYS_KW, THE_DEV_LOGER_PREFIX

SYS_KW[THE_DEV_LOGER_PREFIX] = sys.argv[1] if len(sys.argv) > 1 else "dev"
from common.third_util.http import run
from common.util.export import File, logger


def start():
    HTTP_CONF_FiLE = File(f"config/setting/{sys.argv[1]}.json")
    logger.info(HTTP_CONF_FiLE)
    conf = HTTP_CONF_FiLE.read_file()
    File(f"data/proc/{sys.argv[1]}.pid").write_file(str(os.getpid()))
    run(conf["py_modules"], port=conf.get("port", 9999))


if __name__ == "__main__":
    start()
