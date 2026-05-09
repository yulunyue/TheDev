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
            (0, 0): [[0, 1, 3, 2], [18, 14, 10, 6], [19, 15, 11, 7]],
            (0, 1): [[20, 21, 23, 22], [16, 12, 8, 4], [17, 13, 9, 5]],
            (1, 0): [[4, 5, 7, 6], [1, 16, 10, 23], [17, 8, 22, 3]],
            (1, 1): [[12, 13, 15, 14], [18, 0, 21, 11], [9, 19, 2, 20]],
            (2, 0): [[8, 9, 11, 10], [5, 2, 12, 20], [7, 3, 14, 21]],
            (2, 1): [[16, 17, 19, 18], [0, 15, 22, 4], [1, 13, 23, 6]],
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
