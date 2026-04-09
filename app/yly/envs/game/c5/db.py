from common.tool.export import (
    ConfigBase,
    StrModel,
    NumberModel,
    ListModel,
    FileConfig,
    SearchModel,
    SelectModel,
)
from .model.chess_state_map import CHESS_MAP_CLS_FUNC, CState333


class Bd(FileConfig):
    name = SearchModel(default_value="default")
    size = SelectModel(default_value=CState333.__name__).set_options(
        *CHESS_MAP_CLS_FUNC.keys()
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
        cls = CHESS_MAP_CLS_FUNC[self.size.get_value()]
        return cls.set_board(self.records.get_value())


Bd.set_resource("data/game/chess.json")
