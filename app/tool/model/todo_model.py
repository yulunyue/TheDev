from common.tool.export import (
    FileConfig,
    StrModel,
    SearchModel,
    NumberModel,
    SelectModel,
    BoolModel,
    DateModel,
)

from common.util.export import Node, C
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
