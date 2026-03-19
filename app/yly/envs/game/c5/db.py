from common.tool.export import ConfigBase, StrModel, NumberModel, ListModel


class Bd(ConfigBase):
    name = StrModel()
    size = NumberModel()
    records = ListModel()
