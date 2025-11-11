from common.algo.base.bin_util import decode_data, encode_data, set_mask
from common.util.export import math, List


class Constant:
    SHAPES = [
        [7, 7],
        [8, 9],
    ]

    DR = [
        [-1, 0],
        [1, -1],
        [1, 1],
        [0, 1],
    ]  # x,y
    IN_ROW = 4
    NULL_POS = 2
    CALC_SCORE_MAX_DEPTH = 1
    SCORES = [
        [0, 10**4, 10**2, 0, -(10**3), -10],
        [0, -(10**3), -10, 0, 10**4, 10**2],
    ]

    def mask_decode(self, s):
        return decode_data(s, [self.SIZE])

    def mask_encode(self, board, shape, low, player_id):
        boare = set_mask(board, low, low + 2, player_id + 2)
        return encode_data([boare, shape, 1 - player_id], self.POS_MASK)

    def pos_score(self, x):
        mid = (self.WIDTH - 1) / 2
        return mid - abs(x - mid)

    def mask_to_grid(self, state):
        ret = [0] * ((self.HEIGHT - 1) * self.WIDTH)
        for i in range(C.WIDTH):
            s: int = state & C.MASK_HEIGHT
            h = s.bit_length()
            for j in range(h - 2, -1, -1):
                if s & self.MASK_POS[j]:
                    ret[j * C.WIDTH + i] = 2
                else:
                    ret[j * C.WIDTH + i] = 1
            state = state >> C.HEIGHT
        return ret


C = Constant()
