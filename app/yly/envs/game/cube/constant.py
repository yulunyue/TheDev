from common.algo.export import encode_data, set_mask
from common.util.export import logger


class Ct:
    SIZE = 6
    SHAPE2 = 2
    AXIS_NUM = 3
    BIT_SIZE = 3
    ACTIONS = {
        SHAPE2: {
            (0, 0): [[0, 1, 3, 2], [4, 16, 12, 8], [17, 13, 9, 5]],
            (0, 1): [[20, 21, 23, 22], [7, 11, 15, 19], [10, 14, 18, 6]],
            (1, 0): [[4, 5, 7, 6], [17, 8, 10, 19], [0, 2, 20, 22]],
            (1, 1): [[12, 13, 15, 14], [3, 16], [9, 1]],
            (2, 0): [[8, 9, 11, 10], [], []],
            (2, 1): [[16, 17, 19, 18], [], []],
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
                # logger.map(k=(i, j), a=a, b=b, v=grid[a])
        return mask


C = Ct().load()
