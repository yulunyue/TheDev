from .constant import C, List


class Env:
    def load(self, s):
        self.HEIGHT, self.WIDTH = C.SHAPES[s]
        self.INIT_MASK = 0
        self.SIZE = self.WIDTH * self.HEIGHT
        self.MASK_FULL = (1 << self.SIZE) - 1
        # self.WIDTH_MASK: List[int] = []
        self.MASK_HEIGHT = (1 << self.HEIGHT) - 1
        self.MASK_POS: List[int] = []
        # self.HEIGHT_CLEAR: List[int] = []
        self.POINTS: List[List[List[int]]] = []
        self.ACTION_SCORE: List[int] = []
        # self.POS_REWARD: List[List[int]] = []
        for i in range(self.HEIGHT):
            self.MASK_POS.append(1 << i)
        for i in range(self.WIDTH):
            pass
            # self.HEIGHT_CLEAR.append(self.MASK_HEIGHT - self.MASK_POS[-1])
        for i in range(self.WIDTH):
            self.INIT_MASK = (self.INIT_MASK << self.HEIGHT) + 1
            # self.WIDTH_MASK.append(
            #     self.MASK_FULL - (self.MASK_HEIGHT << (i * self.HEIGHT))
            # )
            # self.ACTION_SCORE.append(self.pos_score(i))
            self.POINTS.append([])
            for j in range(self.HEIGHT):
                self.POINTS[-1].append([])
                for k, (dy, dx) in enumerate(self.DR):
                    tmp = []
                    for l in range(-3, 4):
                        if l == 0:
                            continue
                        x, y = i + dx * l, j + dy * l
                        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT - 1:
                            continue
                        tmp.append([x, y])
                    if len(tmp) >= 3:
                        self.POINTS[-1][-1].append(tmp)

    def set_shape(self, shape_idx):
        self.load(shape_idx)
        self.widths = [0] * C.WIDTH
        self.heights = [0] * C.WIDTH
        self.grid = [[C.NULL_POS] * C.HEIGHT for _ in range(C.WIDTH)]
        self.step = 0
        self.state = C.INIT_MASK
        return self

    def set_state(self, state: int):
        if self.state == state:
            return self
        for i in range(C.WIDTH):
            s1: int = state & C.MASK_HEIGHT

            self.set_column(i, s1)
        return self

    def set_column(self, i, s1: int):
        if s1 == self.widths[i]:
            return self
        step = s1.bit_length() - 1
        self.step += step - self.heights[i]
        s = s1
        for j in range(step):
            self.set_pos(i, j, s & 1)
            s = s >> 1
        for j in range(step, C.HEIGHT):
            self.set_pos(i, j, -1)
        self.heights[i] = step
        self.widths[i] = s1

    def set_pos(self, i, j, s):
        pass


ENV = Env()
