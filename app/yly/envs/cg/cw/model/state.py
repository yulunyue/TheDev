from common.algo.search.state import State
from ..shape.world import World


class CwState(State):
    g: World = None

    def __init__(self, state: str):
        super().__init__(state)
        self.g.set_shapes(state.split(","))

    def to_str(self):

        s = self.show_msgs + [
            [C.WALL_S] * (self.width + 1),
        ]
        for i, row in enumerate(self.grid):
            tmp = ["*"]
            for j, c in enumerate(row):
                tmp.append(c.view())
            tmp.append("*")
            s.append(tmp)
        s.append([C.WALL_S] * (self.width + 1))
        acs = [str(a) for a in self.get_sort_actions()]

        return "\n".join(["".join(r) for r in s] + acs)

    def get_reward(self, **kw):
        return 0
