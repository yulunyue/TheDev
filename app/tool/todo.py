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
        todos = []
        money = 342700
        models: List[TodoModel] = sorted(
            self.model.all(), key=lambda v: v.create_time.get_value(), reverse=True
        )
        score_map = dict(study=1, entertainment=-3, life=2, sport=3, project=2)
        score = 0
        for v in models:
            if v.category == "money":
                money -= float(v.content.get_value())
            if v.category == category and v.done == done:
                todos.append(v)
            if v.done.get_value() and v.user_id == self.username:
                score += score_map.get(v.category.get_value(), 0)
        money = "".join(list(str(int(money)))[::-1])
        return Node(childs=todos, title=f"分数: {score}.{money}")

    def hander(self, key, type, value: dict):
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
