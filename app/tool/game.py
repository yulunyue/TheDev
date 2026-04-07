from ..yly.envs.game.c5.db import Bd
from ..yly.envs.game.c5.player.al import Al
from common.tool.export import FontSearch, FormBase
from common.util.export import IO_MANAGE, ApiBase, Node


AI_PLAYER = {"ad3", "mc100"}


class ChessF5(FormBase, ApiBase):
    model = Bd

    def to_form_row_view(self):
        return FormBase().to_form_row_view().set_btns(save="保存", deduction="推演")

    def web_search(self, key, name, **kw):
        if key == Bd.name.__name__:
            return super().web_search(key, name, **kw)
        return FontSearch().add_node(AI_PLAYER)

    def web_submit(self, type, value, **kw):
        c = Bd.insert(value)
        Bd.get_state()
        if type == "save":
            pass
        return Node()

    def play(self, name, y, x, **kw):
        Al.get_player()
        c: Bd = Bd.get(name)
        c.p0.set_value_if_none(self.username)
        c.p1.set_value_if_none(self.username)
        c.records.append(c.size.get_value() * y + x)
        c.save()
        return c
