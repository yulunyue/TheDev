import sys
from common.export import run, MainHander, install, check, PORT, manage, File

from app.tool.export import api, file, TASK_MANAGER, user

GS = [manage, file, api, user]
HTTP_CONF_FiLE = File("data/setting/http.json")
if HTTP_CONF_FiLE.exists():
    data = HTTP_CONF_FiLE.read_file()
    GS.extend(data["py_modules"])
    TASK_MANAGER.load(data["task"]).start()

if __name__ == "__main__":
    if sys.argv[1] == "install":
        install()
    elif sys.argv[1] == "check":
        check()
    elif sys.argv[1] == "run":
        run(GS, port=PORT)
