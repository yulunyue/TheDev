from ..shape.cell9 import Cell9, C
from ..constant import TcEnum
from common.algo.search.state import State, Action,MctsState
from common.util.export import Dict, List



CELL = Cell9(0)


class TtState3(MctsState):
    def __init__(self, state):
        CELL.set_state(state)
        depth = CELL.ct_num[1] + CELL.ct_num[2]
        self.set_done(CELL.get_done()).set_reward(CELL.get_reward())
        super().__init__(state, depth%2, depth)
 

    def make_actions(self, depth=1, **kw):
        actions = dict()
        CELL.set_state(self.state)
        cells = list(CELL.cell_map[C.PLAYER_NULL].values())
        for a in cells:
            s2 = self.state | C.STATE_KEYS[a.key][self.player_id]
            ac = Action(self, a.key, TtState3.new(s2))
            actions[a.key] = ac
        return actions

    def to_str(self):
        CELL.set_state(self.state)
        ret = [["."] * 3 for _ in range(3)]
        for c in CELL.cells:
            y, x = c.key // 3, c.key % 3
            ret[y][x] = C.VIEW_STR[c.value]
        return "\n".join(["".join(row) for row in ret])




