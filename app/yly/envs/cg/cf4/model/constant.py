from common.algo.base.bin_util import decode_data, encode_data, set_mask
from common.util.export import math, List


class Cases:
    CASE1 = 0xF000000000000000700


CASES = Cases()


class Constant:
    SHAPES = [[7, 7], [8, 9]]

    DR = [[0, 1], [1, 0], [1, -1], [1, 1]]
    IN_ROW = 4
    SCORE2 = 0.002
    SCORE3 = 0.05

    def load(self, s):
        self.HEIGHT, self.WIDTH = self.SHAPES[s]
        self.SIZE = self.WIDTH * self.HEIGHT
        self.MASK_SIZE = (1 << self.SIZE) - 1
        self.MASK_HEIGHT = (1 << self.HEIGHT) - 1
        self.MASK_POS: List[List[int]] = []
        self.POS_REWARD = [] 
        for i in range(self.WIDTH):
            s = 1 << (i * self.HEIGHT)
            self.MASK_POS.append([])
            for j in range(self.HEIGHT):
                self.MASK_POS[-1].append(s << j)

    def mask_decode(self, s):
        return decode_data(s, [self.SIZE])

    def mask_encode(self, board, shape, low, player_id):
        boare = set_mask(board, low, low + 2, player_id + 2)
        return encode_data([boare, shape, 1 - player_id], self.POS_MASK)

    def pos_score(self, y, x):
        h, w = self.SHAPES[1]
        yc, xc = abs(h / 2 - y), abs(w / 2 - x)
        c = math.sqrt(yc * yc + xc * xc)
        return c * 0.0000002


C = Constant()
