from common.tool.export import (
    FormBase,
    TaskConfig,
    TASK_MANAGE,
)
from common.util.export import C, IO_MANAGE


class TaskCg(TaskConfig):
    @classmethod
    def save_to_local(cls):
        super().save_to_local()


TaskCg.set_resource("config/setting/task.json")


class TaskManage(FormBase):
    model = TaskCg
