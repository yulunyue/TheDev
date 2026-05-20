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
from common.util.export import Node, Type, time, get_log
from .model.todo_model import TodoModel

logger = get_log("todo")


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
        score, money, todos = TodoModel.search(category, done)
        return Node(children=todos, title=f"分数: {score}.{money}")

    def _handler_insert(self, _id, value):
        category = value.get("category")
        options = self.model.category.get_options()
        if category not in options:
            raise Exception(
                f"category {category} not in {list(options.keys())} "
            )
        if self.model.exist(_id):
            raise Exception(f"{_id} exist")
        value.update(create_time=time.time(), user_id=self.username)
        return value

    def _handler_edit(self, _id, value):
        category = value.get("category")
        options = self.model.category.get_options()
        if category not in options:
            raise Exception(
                f"category {category} not in {list(options.keys())} "
            )
        d = self.model.query(value["title"])
        user_id = d.user_id.get_value()
        if user_id and user_id != self.username:
            raise Exception("not allow")
        value.update(update_time=time.time(), user_id=self.username)
        return value

    def _handler_delete(self, _id, value):
        return value

    def web_clone(self, **value):
        category = value.get("category")
        options = self.model.category.get_options()
        if category not in options:
            raise Exception(
                f"category {category} not in {list(options.keys())} "
            )
        now_time = time.time()
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
        return Node(value=True)

    def upload_msg(self, **params):
        logger.info(f"upload_msg params: {params}")
        return Node(value=True)
