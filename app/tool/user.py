from common.tool.export import (
    FileConfig,
    StrModel,
    EncroyModel,
    SearchModel,
    NumberModel,
    SelectModel,
)


class User(FileConfig):
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


User.set_resource("config/setting/user.json")
