from .constant import C


class Env:
    def set_shape(self, shape_idx):
        C.set_shape(shape_idx)
        self.widths = [0] * C.WIDTH
        self.heights = [0] * C.WIDTH
        self.step = 0
        self.state = C.INIT_MASK
        return self

    def set_state(self, state):
        s: int = self.state
        for i in range(C.WIDTH):
            s1: int = s & C.MASK_HEIGHT
            if s1 == self.widths[i]:
                continue
            step = s1.bit_length() - 1
            self.step += step - self.heights[i]
            self.heights[i] = step
            self.widths[i] = s1


ENV = Env()
