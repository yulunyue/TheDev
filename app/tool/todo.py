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
from common.util.export import Node


class TodoModel(FileConfig):
    title = StrModel()
    content = StrModel()
    category = SelectModel().set_options("study", "entertainment")
    done = BoolModel(default_value=False)
    priority = NumberModel(default_value=0)
    create_time = DateModel()
    update_time = DateModel()


TodoModel.set_resource("config/setting/todo.json")


class Todo(FormBase):
    model = TodoModel

    def web_search(self, key, name, **kw):
        return Node(
            childs=[dict(title=v._id, value=v) for v in self.__class__.model.all()]
        )

    def get_score(self, **kw):
        score = 0
        for todo in self.__class__.model.all():
            if todo.done.get_value():
                if todo.category.get_value() == "study":
                    score += 1
                elif todo.category.get_value() == "entertainment":
                    score -= 1
        return Node(value=score)

    def get_stats(self, **kw):

        study_done = []
        study_pending = []
        entertainment_done = []
        entertainment_pending = []
        for todo in self.__class__.model.all():
            category = todo.category.get_value()
            is_done = todo.done.get_value()
            if category == "study":
                if is_done:
                    study_done.append(todo)
                else:
                    study_pending.append(todo)
            else:
                if is_done:
                    entertainment_done.append(todo)
                else:
                    entertainment_pending.append(todo)
        return Node(
            childs=[
                dict(
                    title="学习已完成",
                    childs=[dict(title=v._id, value=v) for v in study_done],
                ),
                dict(
                    title="学习未完成",
                    childs=[dict(title=v._id, value=v) for v in study_pending],
                ),
                dict(
                    title="娱乐已完成",
                    childs=[dict(title=v._id, value=v) for v in entertainment_done],
                ),
                dict(
                    title="娱乐未完成",
                    childs=[dict(title=v._id, value=v) for v in entertainment_pending],
                ),
            ],
            value=self.get_score().value,
        )
