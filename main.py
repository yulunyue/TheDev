from common.service.http import run
from common.service.task import Task
from app.yly import manage
if __name__ == '__main__':
    Task().start()
    run(manage)
