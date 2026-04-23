from common.tool.export import (
    FileConfig,
    StrModel,
    SearchModel,
    NumberModel,
    SelectModel,
    BoolModel,
    DateModel,
    FormBase,
)


class TodoModel(FileConfig):
    title = StrModel()
    content = StrModel()
    status = SelectModel().set_options("pending", "doing", "done", "closed")
    priority = NumberModel(default_value=0)
    done = BoolModel(default_value=False)
    create_time = DateModel()
    update_time = DateModel()


TodoModel.set_resource("config/setting/todo.json")


class Todo(FormBase):
    model = TodoModel