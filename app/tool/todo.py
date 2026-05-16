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
from .model.todo_model import TodoModel


class Todo(FormBase):
    model: Type[TodoModel] = TodoModel

    def schema(self):
        return Node(
            data=dict(
                top_form=self.to_form_column_view(),
                category=TodoModel.category,
            )
        )

    def web_search(self, category, done, **kw):
        score, money, todos = TodoModel.search(category, done, self.username)
        money_str = "".join(list(str(money))[::-1])
        return Node(children=todos, title=f"分数: {score}.{money_str}")

    def handler(self, key, type, value: dict):
        category = value.get("category")
        now_time = time.time()
        if category not in self.model.category.options:
            raise Exception(
                f"category {category} not in {list(TodoModel.category.options.keys())} "
            )
        if category == "money":
            value.update(content=float(value["content"]))
        if type == C.METHOD_INSERT:
            if self.model.exist(key):
                raise Exception(f"{key} exist")
            value.update(create_time=now_time, user_id=self.username)
        elif type == C.METHOD_EDIT:
            d = self.model.query(value["title"])
            user_id = d.user_id.get_value()
            if user_id and user_id != self.username:
                raise Exception("not allow")
            value.update(update_time=now_time, user_id=self.username)
        elif type == C.METHOD_CLONE:
            content = value["content"]
            if not content or self.model.exist(content):
                raise Exception(f"contnet is error {content}")
            self.model.query(value["title"]).update(
                done=True, content=f"NEXT:{content}", update_time=now_time
            )
            self.model.insert(
                content,
                title=content,
                category=category,
                create_time=now_time,
                user_id=self.username,
            )
            self.model.save_to_local()
        elif type != C.METHOD_DELETE:
            raise Exception(type)
        return value
