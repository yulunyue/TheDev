from ..yly.envs.game.c5.db import Bd
from common.tool.export import FontSearch
from common.util.export import IO_MANAGE, ApiBase
from .template.front import FormBase


class ChessF5(FormBase, ApiBase):
    model = Bd

    def fight(self):
        pass

    def play(self, name, y, x, **kw):
        c: Bd = Bd.get(name)
        c.player_0.set_value_if_none(self.username)
        c.player_1.set_value_if_none(self.username)
        c.records.append(c.size.get_value() * y + x)
        c.save()
        return c
