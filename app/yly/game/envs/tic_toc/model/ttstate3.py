from ..shape.cell9 import Cell9, C
from ..constant import TcEnum
from common.algo.search.state import State, Action
from common.util.export import Dict, List

CELL = Cell9()


class TtState3(State):
    S: Dict[int, "TtState3"] = dict()

    @classmethod
    def new(cls, state=0):
        if state not in TtState3.S:
            TtState3.S[state] = TtState3(state)
        return TtState3.S[state]

    def get_actions(self, depth=1, **kw):
        if self.actions is not None:
            return self.actions
        env = self.get_env()
        self.actions = dict()
        for a in env.cell_map[C.PLAYER_NULL].values():
            s2 = CELL.get_state(a, self.player_id)
            ac = Action(self, a.key, TtState3.new(s2))
            self.actions[a.key] = ac.set_reward(0)
        return self.actions

    def get_env(self):
        CELL.set_state(self.state)
        self.depth = CELL.ct_num[1] + CELL.ct_num[2]
        self.data = CELL.state_count.copy()
        self.player_id = 1 + self.depth % 2
        self.set_done(CELL.get_done())
        return CELL

    def to_str(self):
        self.get_env()
        ret = [["."] * 3 for _ in range(3)]
        for c in self.get_env().cells:
            y, x = c.key // 3, c.key % 3
            ret[y][x] = C.VIEW_STR[c.value]
        return "\n".join(["".join(row) for row in ret])

    def get_done(self):
        self.get_env()
        return self.done

    def get_reward(self, actions: List[Action], params: TcEnum, **kw):
        self.get_env()
        reward = 0
        for p in params.get_params().values():
            reward += p.get_value() * self.data[p.key]
        return reward
