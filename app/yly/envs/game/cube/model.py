from common.algo.export import State, encode_data, decode_data, Action
from common.third_util.ml.np_util import np
from common.util.export import logger, List, Dict
from .constant import C


class CubeAction(Action):
    def show(self, msg=None):
        c, d, r, *args = self.action
        if r == -1:
            r = 3

        return super().show(f"第{d}层{C.COLORS[c]}色-顺时针旋转{r}圈")


class CubeState(State):
    def __init__(self, state, depth=0):
        super().__init__(state, depth=depth)
        self.grid = decode_data(state, [C.BIT_SIZE] * (C.SIZE * C.n * C.n))

    STATE_STORE: Dict[str, "CubeState"] = dict()

    @classmethod
    def new_shape(cls, n) -> "CubeState":
        C.load(n)
        return CubeState.new(C.init_mask)

    def game_over(self):
        return self.state == C.init_mask

    def make_actions(self) -> List[CubeAction]:
        ret = []
        for i in range(C.AXIS_NUM):
            for j in range(C.n):
                for a in C.MOVE_ACTION:
                    mask = C.get_converts(self.state, i, j, a, self.grid)
                    new_state = CubeState(mask, depth=self.depth + 1)
                    action = CubeAction(self, (i, j, a, len(ret)), new_state)
                    ret.append(action)
        return ret

    def to_str(self, *args, **kw):
        ans = [["  "] * (C.n * 4) for _ in range(C.n * 3)]
        for u in range(len(self.grid)):
            i, k = u // (C.n * C.n), u % (C.n * C.n)
            if i == 0:
                y, x = 0, C.n
            elif i == C.SIZE - 1:
                y, x = 2 * C.n, C.n
            else:
                y, x = C.n, (i - 1) * C.n
            ic, jc = k // C.n, k % C.n
            ii, jj = y + ic, x + jc
            # ans[ii][jj] = f"{i}{self.grid[u]}"
            ans[ii][jj] = C.COLORS[self.grid[u]]
        return ["".join(v) for v in ans]

    def to_json(self) -> dict:
        return {
            "state": self.state,
            "depth": self.depth,
            "n": C.n,
            "game_over": self.game_over(),
        }

    def load_from_json(self, data: dict):
        if "n" in data:
            C.load(data["n"])
        self.state = data["state"]
        self.depth = data.get("depth", 0)
        return self
