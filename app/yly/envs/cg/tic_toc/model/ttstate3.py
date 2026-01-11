from common.algo.search.state import AbState, Action, State
from common.util.export import Dict, List
from .ttaction import TtAction
from ..constant import C


class TtState3(AbState):
    def load(self):
        self.depth = self.state.bit_count()
        self.player_id = self.depth % 2
        if self.depth == C.ALL_SIZE3:
            self.done = State.NO_WIN
        for ln in C.lines[1 - self.player_id]:
            if (ln & self.state).bit_count() == 3:
                self.done = (
                    State.FIRST_WIN if self.player_id == 1 else State.SECONEND_WIN
                )
                break
        return self

    @classmethod
    def new(cls, state) -> "TtState3":
        return super().new(state).load()

    def make_actions(self, **kw):
        actions = []
        for i in range(C.ALL_SIZE3):
            s2 = self.state & C.STATE_KEYS[i]
            if s2:
                continue
            s2 = self.state | ((self.player_id + 1) << (i * 2))
            s = TtState3.new(s2)
            ac = Action(self, i, s).set_reward(0)
            if s.done == 1 + self.player_id:
                ac.set_reward(1)
            actions.append(ac)
        return actions

    def to_str(self):
        ret = [["."] * 3 for _ in range(3)]
        for i in range(C.ALL_SIZE3):
            y, x = i // 3, i % 3
            s = (self.state >> (i * 2)) & 3
            ret[y][x] = C.VIEW_STR[s]
        return ["".join(row) for row in ret]
