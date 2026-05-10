from ..yly.envs.game.c5.db import Bd as FontBd, ROUTE_PATH
from ..yly.envs.game.c5.player.al import Al
from common.tool.export import FontSearch, FormBase
from common.util.export import IO_MANAGE, ApiBase, Node, C

AI_PLAYER = {"ad3", "mc100"}


class ChessF5(FormBase, ApiBase):
    model = FontBd
    ROUTE_PATH = ROUTE_PATH

    def search_name(self, *args, **kw):
        return FontSearch().add_node(FontBd.instance_map.keys())

    def to_form_column_view(self):
        return (
            super()
            .to_form_column_view()
            .set_btns(
                **{
                    C.METHOD_ROLL_BACK: "悔棋",
                    C.METHOD_DELETE: "模拟",
                }
            )
        )

    def search_algo(self, *args, **kw):
        return FontSearch().add_node(
            list(AI_PLAYER) + list(IO_MANAGE.get_users_by_topic(C.TOPIC_F5_CHESS))
        )

    def web_submit(self, type, value, **kw):
        name = value.get("name", "default")
        c = FontBd.insert(name, **value)
        childs = []
        if type == "save":
            FontBd.save()
        elif type == "simulation":
            if c.p0.get_value() not in AI_PLAYER or c.p1.get_value() not in AI_PLAYER:
                raise Exception(f"只有玩家{AI_PLAYER}可以模拟")
            s = c.get_state()
            al = Al().set_state(s)
            al.actor([c.p0.get_value(), c.p1.get_value()])
            records = [a.action for a in al.record_actions]
            c.records.set_value(records)
            FontBd.save()
            childs = records
        return Node(childs=childs)

    def play(self, name, y, x, **kw):
        c: FontBd = FontBd.get(name)
        board = c.get_state()
        idx = board.env.yx_to_idx(y, x)
        if idx not in board.can_moves:
            raise Exception(f"位置({y}, {x})不可用")
        action = board.get_action(idx)
        records = c.records.get_value()
        records.append(idx)
        c.records.set_value(records)
        c.save()
        result = c.to_json()
        IO_MANAGE.send(
            f"{C.TOPIC_TASK_UPDATE_MSG}.{name}",
            result,
        )
        return Node(value=result)
