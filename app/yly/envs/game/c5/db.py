from common.tool.export import ConfigBase, StrModel, NumberModel, ListModel, FileConfig


class Bd(FileConfig):
    name = StrModel()
    size = NumberModel()
    records = ListModel()


Bd.init_param()
