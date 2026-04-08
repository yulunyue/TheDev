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
from .model.chess_static import ChessState


class Bd(FileConfig):
    name = SearchModel(default_value="default")
    size = SelectModel(default_value="size_3x3x3").set_options(
        size_3x3x3=dict(width=3, height=3, in_row=3),
    )
    records = ListModel()
    p0 = SearchModel(default_value="ad3")
    p1 = SearchModel(default_value="ad3")

    @classmethod
    def get_font_columns(cls):
        return [cls.name, cls.size, cls.p0, cls.p1]

    @classmethod
    def get_id(cls, *args, name="", **kw):
        return str(name)

    def get_state(self):
        w = self.size.get_data()
        return ChessState.set_board(
            *size,
        )


Bd.set_resource("data/game/chess.json")
