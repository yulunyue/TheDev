from common.algo.export import encode_data, set_mask
from common.util.export import logger


class Ct:
    WHITE = 0
    RED = 2
    ORANGE = 3
    GREEN = 4
    LEFT = 5
    YELLOW = 1
    SIZE = 6
    SHAPE2 = 2
    BIT_SIZE = 3
    ACTIONS = {
        SHAPE2: {
            (0, 0): [[2, 0, 1, 3], [8, 4, 16, 12], [9, 5, 17, 13]],
            (0, 1): [[20, 22, 23, 21], [10, 6, 18, 14], [11, 7, 19, 15]],
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
        ar1 = self.ACTIONS[self.n].get((i, j), [])
        if not ar1:
            return mask
        for a2 in ar1:
            for ii, a in enumerate(a2):
                b = self.all_size - 1 - a2[(ii + tp) % len(a2)]
                mask = set_mask(mask, b * self.BIT_SIZE, self.BIT_SIZE, grid[a])
                # logger.map(k=(i, j), a=a, b=b, v=grid[a])
        return mask


C = Ct().load()
