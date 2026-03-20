from common.tool.export import (
    ConfigBase,
    StrModel,
    NumberModel,
    ListModel,
    FileConfig,
    SearchModel,
)


class Bd(FileConfig):
    name = SearchModel()
    size = NumberModel()
    records = ListModel()

    @classmethod
    def get_font_columns(cls):
        return [cls.name, cls.size]


Bd.init_param()
