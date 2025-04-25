from typing import Dict, List
from common.algo.search.state import State, Action, inf
from app.yly.algo.cg.cf4.constant import C, S


class F4State(State):

    def __init__(self):
        super().__init__(0, 0)

    def init_root(self, state=None):
        self.state = state
        self.load_root()
        return self

    def load_root(self):
        pass

    def get_actions_all(self):
        return range(C.WIDTH)

    def grid_to_str(self):
        grid = self.get_grid()
        h, w = C.HEIGHT, C.WIDTH
        ret = []
        for i in range(h):
            tmp = []
            for j in range(w):
                v = grid[i * w + j]
                if isinstance(v, int) and 1 <= v <= 2:
                    tmp.append(f"-{S[v-1]}")
                else:
                    tmp.append("- ")
            ret.append("".join(tmp))
        return "\n".join(ret)

    def get_grid(self):
        pass

    def to_str(self):
        return "\n".join(["", self.grid_to_str(), ""])

    def __str__(self):
        return self.to_str()
