from common.tool.export import (
    ConfigBase,
    StrModel,
    NumberModel,
    ListModel,
    FileConfig,
    SearchModel,
    SelectModel,
)
from .board.base_state import BoardC5State


class Bd(FileConfig):
    name = SearchModel()
    size = SelectModel().set_options(3, 4, 6, 10)
    records = ListModel()
    p0 = SearchModel()
    p1 = SearchModel()

    @classmethod
    def get_font_columns(cls):
        return [cls.name, cls.size, cls.p0, cls.p1]

    @classmethod
    def get_id(cls, name, **kw):
        return str(name)

    def get_state(self):
        s = BoardC5State()


Bd.set_resource("data/game/chess.json")
