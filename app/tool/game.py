from ..yly.envs.game.c5.db import Bd
from ..yly.envs.game.c5.player.al import Al
from common.tool.export import FontSearch, FormBase
from common.util.export import IO_MANAGE, ApiBase, Node


AI_PLAYER = {"ad3", "mc100"}


class ChessF5(FormBase, ApiBase):
    model = Bd

    def to_form_row_view(self):
        return FormBase().to_form_row_view().set_btns(save="保存", simulation="模拟")

    def web_search(self, key, name, **kw):
        if key == Bd.name.__name__:
            return super().web_search(key, name, **kw)
        return FontSearch().add_node(list(AI_PLAYER) + IO_MANAGE.get_all_users())

    def web_submit(self, type, value, **kw):
        c = Bd.insert(**value)
        childs = []
        if type == "save":
            pass
        elif type == "simulation":
            if c.p0.get_value() not in AI_PLAYER or c.p1.get_value() not in AI_PLAYER:
                raise Exception(f"只有玩家{AI_PLAYER}可以模拟")
            s = c.get_state()
            al = Al().set_state(s)
            al.actor([c.p0.get_value(), c.p1.get_value()])
            childs = [a.action for a in al.record_actions]
        return Node(childs=childs)

    def play(self, name, y, x, **kw):
        c: Bd = Bd.get(name)
        s = c.get_state()
        return c
