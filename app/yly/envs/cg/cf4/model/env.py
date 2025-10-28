from .constant import C


class Env:
    def set_shape(self, shape_idx):
        C.set_shape(shape_idx)
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
