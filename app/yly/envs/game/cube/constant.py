from common.algo.export import encode_data, set_mask
from common.util.export import logger


class Ct:
    SIZE = 6
    SHAPE2 = 2
    AXIS_NUM = 3
    BIT_SIZE = 3
    COLOR_RED = 0
    COLORS = ["B", "O", "W", "R", "Y", "G"]
    ACTIONS = {
        SHAPE2: {
            (0, 0): [[0, 1, 3, 2], [16, 4, 8, 12], [17, 5, 9, 13]],
            (0, 1): [[20, 21, 23, 22], [10, 14, 18, 6], [11, 15, 19, 7]],
            (1, 0): [[12, 13, 15, 14], [1, 3, 23, 21], [9, 11, 17, 19]],
            (1, 1): [[4, 5, 7, 6], [0, 2, 22, 20], [8, 17, 19, 10]],
            (2, 0): [[8, 9, 11, 10], [0, 1, 21, 20], [5, 13, 15, 7]],
            (2, 1): [[16, 17, 19, 18], [2, 3, 23, 22], [4, 12, 14, 6]],
        },
    }

    MOVE_ACTION = [-1, 1, 2]

    def load(self, n=SHAPE2):
        self.n = n
        self.init_mask = self.new_shape_state(n)
        self.all_size = self.n * self.n * self.SIZE
        return self

    def new_shape_state(self, n):
        array = []
        for i in range(self.SIZE):
            array.extend([i] * (n * n))
        return encode_data(array, self.BIT_SIZE)

    def get_converts(self, mask, i, j, tp, grid):
        ar1 = self.ACTIONS[self.n][(i, j)]
        for a2 in ar1:
            for ii, a in enumerate(a2):
                b = self.all_size - 1 - a2[(ii + tp) % len(a2)]
                mask = set_mask(mask, b * self.BIT_SIZE, self.BIT_SIZE, grid[a])
        return mask


C = Ct().load()
