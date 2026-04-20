from common.tool.export import (
    FileConfig,
    StrModel,
    EncroyModel,
    SearchModel,
    NumberModel,
    SelectModel,
    FormBase,
    TaskConfig,
    TASK_MANAGE,
)
from common.util.export import C


class TaskManage(FormBase):
    model = TaskConfig
