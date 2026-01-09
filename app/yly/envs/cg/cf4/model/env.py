from .constant import C, List
from app.yly.envs.game.c5.board.base import Constant, set_mask
from common.util.export import logger


class Env(Constant):
    BIT_SIZE = 1

    def set_shape(self, shape_idx):
        w, h = C.SHAPES[shape_idx]
        self.load(w, h, in_row=C.IN_ROW)
        self.INIT_MASK = 0
        for _ in range(self.width):
            self.INIT_MASK = (self.INIT_MASK << self.height_bit) + 1
        self.state = self.INIT_MASK
        return self

    def init_size(self):
        self.size = self.width * (self.height - 1)

    def get_next_state(self, old_state: int, pos: int, player_id: int):
        state = (old_state >> (pos * self.height_bit)) & self.mask_row
        bit_length = state.bit_length()
        if bit_length == self.height:
            return None, None
        idx = bit_length + pos * self.height - 1
        s = set_mask(old_state, idx * self.BIT_SIZE, 2, player_id + 2)
        return bit_length - 1 + pos * self.get_loop2(), s

    def get_yx(self, i):
        return self.get_loop2() - 1 - (i % self.get_loop2()), i // self.get_loop2()

    def change_col(self, x, state3: int, state4: int):
        h = state4.bit_length()
        for y in range(self.get_loop2()):
            idx = x * self.get_loop2() + y
            if y >= h - 1:
                player_id = 0
            else:
                player_id = (state4 & self.mask_bit) + 1
            self.set_pos_player_id(idx, player_id)
            state4 = state4 >> self.BIT_SIZE

    def get_loop1(self):
        return self.width

    def get_loop2(self):
        return self.height - 1


ENV = Env()
