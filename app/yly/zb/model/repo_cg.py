from .util import ConfigBase, StrModel, ListModel, DictModel, NumberModel


class RepoCg(ConfigBase):
    py_name = StrModel()
    base_commit = StrModel()
