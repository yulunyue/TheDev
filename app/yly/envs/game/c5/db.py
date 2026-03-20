from common.tool.export import ConfigBase, StrModel, NumberModel, ListModel, FileConfig


class Bd(FileConfig):
    name = StrModel()
    size = NumberModel()
    records = ListModel()

    @classmethod
    def get_font_columns(cls):
        return [cls.name, cls.size]


Bd.init_param()
