from common.tool.export import FormBase, TaskConfig, Task, TASK_MANAGE
from common.util.export import C, IO_MANAGE
import time


class TaskManage(FormBase, Task):
    model = TaskConfig


TASK_MANAGE.set_resource("config/setting/task.json").start()
