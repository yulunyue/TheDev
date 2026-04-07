from ..yly.envs.game.c5.db import Bd
from common.tool.export import FontSearch, FormBase
from common.util.export import IO_MANAGE, ApiBase


class ChessF5(FormBase, ApiBase):
    model = Bd

    def play(self, name, y, x, **kw):
        c: Bd = Bd.get(name)
        c.p0.set_value_if_none(self.username)
        c.p1.set_value_if_none(self.username)
        c.records.append(c.size.get_value() * y + x)
        c.save()
        return c
