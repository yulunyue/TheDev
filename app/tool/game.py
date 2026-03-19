from common.tool.export import (
    TableConfig,
    StrModel,
    NumberModel,
    FileConfig,
    FrontTable,
    DateModel,
    ListModel,
)


class ChessConfig:
    name = StrModel()
    size = NumberModel()
    record = ListModel()


class Game:
    pass
