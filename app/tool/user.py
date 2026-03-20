from common.tool.export import (
    FileConfig,
    StrModel,
    EncroyModel,
    SearchModel,
    NumberModel,
)


class User(FileConfig):
    name = SearchModel()
    title = StrModel()
    visite_num = NumberModel(default_value=0)
    password = EncroyModel()


User.set_resource("config/setting/user.json")
