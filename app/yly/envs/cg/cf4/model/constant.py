from common.algo.base.bin_util import decode_data, encode_data, set_mask
from common.util.export import math, List


class Cases:
    CASE1 = 0x7000000000000000700


CASES = Cases()


class Constant:
    SHAPES = [[7, 7], [7, 9]]

    DR = [[0, 1], [1, 0], [1, -1], [1, 1]]
    IN_ROW = 4
    SCORE2 = 0.002
    SCORE3 = 0.05
    POS_SCORE_RADIO = 0.0000002

    def load(self, s):
        self.HEIGHT, self.WIDTH = self.SHAPES[s]
        self.SIZE = self.WIDTH * self.HEIGHT
        self.MASK_SIZE = (1 << self.SIZE) - 1
        self.MASK_HEIGHT = (1 << self.HEIGHT) - 1
        self.MASK_POS: List[List[int]] = []
        self.POS_REWARD: List[List[int]] = []
        for i in range(self.WIDTH):
            s = 1 << (i * self.HEIGHT)
            self.POS_REWARD.append([])
            self.MASK_POS.append([])
            for j in range(self.HEIGHT):
                self.MASK_POS[-1].append(s << j)
                self.POS_REWARD[-1].append(self.pos_score(j, i))

    def mask_decode(self, s):
        return decode_data(s, [self.SIZE])

    def mask_encode(self, board, shape, low, player_id):
        boare = set_mask(board, low, low + 2, player_id + 2)
        return encode_data([boare, shape, 1 - player_id], self.POS_MASK)

    def pos_score(self, y, x):
        b = math.sqrt(self.HEIGHT * self.HEIGHT / 4 + self.WIDTH * self.WIDTH / 4)
        yc, xc = abs(self.HEIGHT / 2 - y), abs(self.WIDTH / 2 - x)
        c = math.sqrt(yc * yc + xc * xc)
        return b - c


C = Constant()
