from common.tool.export import (
    FileConfig,
    StrModel,
    EncroyModel,
    SearchModel,
    NumberModel,
    SelectModel,
    FormBase,
)


class TaskModel(FileConfig):
    name = SearchModel()
    title = StrModel()
    visite_num = NumberModel(default_value=0)
    password = EncroyModel()
    user_type = SelectModel().set_options(0, 1, 2)


TaskModel.set_resource("config/setting/task.json")


class TaskExec(FormBase):
    model = TaskModel
