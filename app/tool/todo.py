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
    title = StrModel().not_null().set_title("项目")
    content = StrModel().set_title("备注")
    category = (
        SelectModel()
        .set_title("类型")
        .set_options(
            study="学习",
            work="工作",
            project="项目",
            money="账本",
            entertainment="娱乐",
            sport="运动",
            life="生活",
        )
        .set_layout(C.LAYOUT_COLUMN)
    )
    done = BoolModel(default_value=False).set_title("状态").set_layout(C.LAYOUT_COLUMN)
    create_time = DateModel()
    update_time = DateModel()
    user_id = SearchModel().set_url("/app/user/web_search").set_title("用户")

    @classmethod
    def get_id_by_param(cls, title, **kw):
        return title

    @classmethod
    def get_form_columns(cls):
        return [cls.title, cls.content, cls.done]


TodoModel.set_resource("config/setting/todo.json")


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
        score_map = dict(study=1, entertainment=-1, life=2, sport=3, project=2)
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
        if category not in TodoModel.category.options:
            raise Exception(
                f"category {category} not in {list(TodoModel.category.options.keys())} "
            )
        if category == "money":
            value.update(content=float(value["content"]))
        if type == C.METHOD_INSERT:
            if TodoModel.exist(key):
                raise Exception(f"{key} exist")
            value.update(create_time=time.time(), update_time=time.time())
        elif type == C.METHOD_EDIT:
            value.update(update_time=time.time(), user_id=self.username)
        elif type != C.METHOD_DELETE:
            raise Exception(type)
        return value
