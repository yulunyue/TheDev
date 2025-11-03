from common.algo.export import State, encode_data, decode_data
from common.third_util.np_util import np
from .constant import C


class CubeState(State):
    def __init__(self, state, n, player_id=0, depth=0):
        super().__init__(state, player_id, depth)
        self.n = n
        grid = decode_data(state, [3] * (C.SIZE * n * n))
        self.grid = np.array(grid).reshape(C.SIZE, n, n)

    @classmethod
    def new_shape(cls, n):
        array = []
        for i in range(C.SIZE):
            array.extend([i] * (n * n))
        mask = encode_data(array, 3)
        return CubeState(mask, n)

    def to_str(self):
        ans = [[" "] * (self.n * 4) for _ in range(self.n * 3)]
        for i in range(C.SIZE):
            if i == 0:
                y, x = 0, self.n
            elif i == C.SIZE - 1:
                y, x = 2 * self.n, self.n
            else:
                y, x = self.n, (i - 1) * self.n
            for k in range(self.n * self.n):
                ic, jc = k // self.n, k % self.n
                ii, jj = y + ic, x + jc
                ans[ii][jj] = str(self.grid[i, ic, jc])
        return [" ".join(v) for v in ans]
