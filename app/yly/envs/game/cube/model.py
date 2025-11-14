from common.algo.export import State, encode_data, decode_data, Action
from common.third_util.np_util import np
from common.util.export import logger
from .constant import C


class CubeState(State):
    def __init__(self, state, player_id=0, depth=0):
        super().__init__(state, player_id, depth)
        self.grid = decode_data(state, [C.BIT_SIZE] * (C.SIZE * C.n * C.n))

    @classmethod
    def new_shape(cls, n):
        C.load(n)
        return CubeState.new(C.init_mask).get_action((0, 0, 1)).get_dst()

    def game_over(self):
        return self.state == C.init_mask

    def make_actions(self):
        ret = []
        for i in range(C.AXIS_NUM):
            for j in range(C.n):
                for a in C.MOVE_ACTION:
                    mask = C.get_converts(self.state, i, j, a, self.grid)
                    action = Action(self, (i, j, a), CubeState.new(mask))
                    ret.append(action)
        return ret

    def to_str(self):
        ans = [[" "] * (C.n * 4) for _ in range(C.n * 3)]
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
            ans[ii][jj] = f"{self.grid[u]}"
        return [" ".join(v) for v in ans]
