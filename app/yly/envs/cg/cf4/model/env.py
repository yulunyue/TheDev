from .constant import C, List
from app.yly.envs.game.c5.constant import Constant, set_mask
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
        self.size = self.width * self.height

    def get_next_state(self, pos: int, player_id: int):
        state = (self.state >> (pos * self.height_bit)) & self.mask_row
        idx = state.bit_length() + pos * self.height_bit - 1
        s = set_mask(self.state, idx * self.BIT_SIZE, 2, player_id + 2)
        return self.get_move_info(idx, player_id), s

    def get_yx(self, i):
        return self.height - 1 - i % self.height, i // self.height

    def is_valide_pos(self, l3, l4):
        return 0 <= l3 < self.get_loop1() and 0 <= l4 < self.get_loop2() - 1

    def change_col(self, x, state4: int):
        h = state4.bit_length()
        for y in range(self.get_loop2()):
            idx = x * self.height + y
            if y >= h - 1:
                player_id = 0
            else:
                player_id = (state4 & self.mask_bit) + 1
            self.set_pos_player_id(idx, player_id)
            state4 = state4 >> self.BIT_SIZE

    def get_loop1(self):
        return self.width

    def get_loop2(self):
        return self.height


ENV = Env()
