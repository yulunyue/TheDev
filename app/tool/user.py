from common.tool.export import (
    FileConfig,
    StrModel,
    EncroyModel,
    SearchModel,
    NumberModel,
    SelectModel,
    FormBase,
)


class UserModel(FileConfig):
    name = SearchModel()
    title = StrModel()
    visite_num = NumberModel(default_value=0)
    password = EncroyModel()
    user_type = SelectModel().set_options(0, 1, 2)

    @classmethod
    def get_id(self, name, **kw):
        if not name:
            return "default"
        return name


UserModel.set_resource("config/setting/user.json")


class User(FormBase):
    model = UserModel
