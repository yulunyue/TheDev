from common.tool.export import (
    FileConfig,
    StrModel,
    EncryptModel,
    SearchModel,
    NumberModel,
    SelectModel,
    FormBase,
    FontSearch,
)


class UserModel(FileConfig):
    name = SearchModel().set_url("/app/user/web_search")
    title = StrModel()
    visite_num = NumberModel(default_value=0)
    password = EncryptModel()
    user_type = SelectModel().set_options(0, 1, 2)


UserModel.set_resource("config/setting/user.json")


class User(FormBase):
    model = UserModel

    def web_search(self, *args, **kw):
        return FontSearch.add_node(UserModel.instance_map.keys())
