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
from common.util.export import Node, C, Type, List, time


class TodoModel(FileConfig):
    title = StrModel().not_null()
    content = StrModel()
    category = SelectModel().set_options("study", "entertainment")
    done = BoolModel(default_value=False)
    create_time = DateModel()
    update_time = DateModel()

    @classmethod
    def get_id_by_param(cls, title, **kw):
        return title

    @classmethod
    def get_form_columns(cls):
        return [cls.title, cls.content, cls.category, cls.done]


TodoModel.set_resource("config/setting/todo.json")


class Todo(FormBase):
    model: Type[TodoModel] = TodoModel

    def web_search(self, category, done, **kw):
        todos = []
        models: List[TodoModel] = sorted(
            self.model.all(), key=lambda v: v.create_time.get_value(), reverse=True
        )
        score_map = dict(study=1, entertainment=-1)
        score = 0
        for v in models:
            if v.category == category and v.done == done:
                todos.append(v)
            if v.done.get_value():
                score += score_map[category]
        return Node(childs=todos, value=score)

    def hander(self, key, type, value: dict):
        category = value.get("category")
        if category not in TodoModel.category.options:
            raise Exception(
                f"category {category} not in {list(TodoModel.category.options.keys())} "
            )
        if type == C.METHOD_INSERT:
            value.update(create_time=time.time(), update_time=time.time())
        elif type == C.METHOD_EDIT:
            value.update(update_time=time.time())
        elif type != C.METHOD_DELETE:
            raise Exception(type)
        return value

    def to_form_row_view(self):
        return (
            super()
            .to_form_row_view()
            .set_btns(C.METHOD_EDIT, C.METHOD_INSERT, C.METHOD_DELETE)
        )
