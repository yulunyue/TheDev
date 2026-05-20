from common.tool.export import (
    FileConfig,
    StrModel,
    SearchModel,
    NumberModel,
    SelectModel,
    BoolModel,
    DateModel,
    FormRow,
)

from common.util.export import Node, C, Type, List


class TodoModel(FileConfig):
    INITIAL_MONEY = 342700

    title = StrModel().not_null().set_title("项目")
    content = StrModel().set_title("备注")
    category = (
        SelectModel()
        .set_title("类型")
        .set_conf_file("config/setting/todo_category.json")
        .set_layout(C.LAYOUT_COLUMN)
    )
    done = BoolModel(default_value=False).set_title("状态").set_width(60)
    create_time = DateModel()
    update_time = DateModel()
    money = NumberModel(default_value=0).set_title("金额")
    score = NumberModel(default_value=0).set_title("分数")
    user_id = SearchModel().set_url("/app/user/web_search").set_title("用户")

    @classmethod
    def get_id_by_param(cls, title, **kw):
        return title

    @classmethod
    def get_form_columns(cls):
        return [
            cls.title,
            cls.content,
            FormRow().set_body(cls.money, cls.score, cls.done),
        ]

    @classmethod
    def calc_score(cls) -> int:
        total = 0
        money = cls.INITIAL_MONEY
        for v in cls.all():
            if v.done.get_value():
                cat_data = v.category.get_data()
                total += cat_data.get("score", 0)
                total += v.score.get_value()
                money -= v.money.get_value()
        return total, money

    @classmethod
    def search(cls, category: str, done: bool) -> "tuple[int, int, List[TodoModel]]":
        models = sorted(
            cls.all(), key=lambda v: v.create_time.get_value(), reverse=True
        )
        todos = []
        for v in models:
            if v.category == category and v.done == done:
                todos.append(v)
        score, money = cls.calc_score()
        return int(score), int(money), todos


TodoModel.set_resource("config/setting/todo.json")
