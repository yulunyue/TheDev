import sys
from common.service.export import run, PORT
from app.tool.export import ROUTES
from common.tool.export import TASK_MANAGER
from common.util.export import File

HTTP_CONF_FiLE = File("data/setting/http.json")
if HTTP_CONF_FiLE.exists():
    data = HTTP_CONF_FiLE.read_file()
    ROUTES = ROUTES + data["py_modules"]
    TASK_MANAGER.load(data["task"]).start()

if __name__ == "__main__":
    run(ROUTES, port=PORT)
