from common.algo.base.bin_util import decode_data, encode_data, set_mask
from common.util.export import math, List


class Cases:
    CASE1 = 0x101010106D4D6D5AA
    CASE2 = 0x101D5D5AAAA060101


CASES = Cases()


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
    SCORE2 = 0.002
    SCORE3 = 0.05
    POS_SCORE_RADIO = 0.0000002

    def load(self, s):
        self.HEIGHT, self.WIDTH = self.SHAPES[s]
        self.INIT_MASK = 0
        self.SIZE = self.WIDTH * self.HEIGHT
        self.MASK_FULL = (1 << self.SIZE) - 1
        self.WIDTH_MASK: List[int] = []
        self.MASK_HEIGHT = (1 << self.HEIGHT) - 1
        self.MASK_POS: List[int] = []
        self.HEIGHT_CLEAR: List[int] = []
        self.POINTS: List[List[List[int]]] = []
        self.POS_SCORE: List[List[int]] = []
        # self.POS_REWARD: List[List[int]] = []
        for i in range(self.HEIGHT):
            self.MASK_POS.append(1 << i)
            self.HEIGHT_CLEAR.append(self.MASK_HEIGHT - self.MASK_POS[-1])
        for i in range(self.WIDTH):
            self.INIT_MASK = (self.INIT_MASK << self.HEIGHT) + 1
            self.WIDTH_MASK.append(
                self.MASK_FULL - (self.MASK_HEIGHT << (i * self.HEIGHT))
            )
            self.POS_SCORE.append([])
            self.POINTS.append([])
            for j in range(self.HEIGHT):
                self.POS_SCORE[-1].append(self.pos_score(i, j))
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

    def mask_decode(self, s):
        return decode_data(s, [self.SIZE])

    def mask_encode(self, board, shape, low, player_id):
        boare = set_mask(board, low, low + 2, player_id + 2)
        return encode_data([boare, shape, 1 - player_id], self.POS_MASK)

    def pos_score(self, x, y):
        d = self.HEIGHT * self.HEIGHT / 4 + self.WIDTH * self.WIDTH / 4
        yc, xc = abs(self.HEIGHT / 2 - y), abs(self.WIDTH / 2 - x)
        c = math.sqrt(yc * yc + xc * xc)
        return math.sqrt(d) - c


C = Constant()
