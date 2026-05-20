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
        value.update(create_time=time.time(), user_id=self.username)
        return value

    def _handler_edit(self, _id, value):
        value.update(update_time=time.time())
        return value

    def web_clone(self, **value):
        category = value.get("category")
        content = value["content"]
        if not content or self.model.exist(content):
            raise Exception(f"contnet is error {content}")
        self.web_edit(title=value["title"], done=True, content=f"NEXT:{content}")
        self.web_insert(
            title=content,
            category=category,
            user_id=self.username,
        )
        return Node(value=True)

    def upload_msg(self, **params):
        logger.info(f"upload_msg params: {params}")
        return Node(value=True)
