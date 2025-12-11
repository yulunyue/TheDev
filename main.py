import sys
import os
from common.util.tool import SYS_KW, THE_DEV_LOGER_PREFIX

SYS_KW[THE_DEV_LOGER_PREFIX] = "main"
from common.service.export import run, PORT
from app.tool.export import ROUTES
from common.util.export import File

HTTP_CONF_FiLE = File("config/setting/http.json")
if HTTP_CONF_FiLE.exists():
    data = HTTP_CONF_FiLE.read_file()
    ROUTES = ROUTES + data["py_modules"]

if __name__ == "__main__":
    run(ROUTES, port=PORT)
