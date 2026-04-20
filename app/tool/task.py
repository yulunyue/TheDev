from common.tool.export import (
    FileConfig,
    StrModel,
    EncroyModel,
    SearchModel,
    NumberModel,
    SelectModel,
    FormBase,
)
from common.util.export import C


class TaskModel(FileConfig):
    name = StrModel()
    state = SelectModel().set_options()
    create_time = NumberModel()
    start_time = NumberModel()
    end_time = NumberModel()


TaskModel.set_resource("config/setting/task.json")


class TaskManage(FormBase):
    model = TaskModel
