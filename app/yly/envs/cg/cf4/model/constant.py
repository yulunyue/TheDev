from common.algo.base.bin_util import decode_data, encode_data, set_mask
from common.util.export import math


class Cases:
    CASE1 = 74076337003370644495
    CASE2 = 74076350232138357855
    CASE3 = 74076350232138357982
    CASE4 = 74077462983057369838
    CASE5 = 74076337003639079951
    ALL = {CASE4: [4, 7, 4, 1]}


CASES = Cases()


class Constant:
    SHAPES = [[7, 7], [8, 9]]
    POS_MASK = [1, 1]
    DR = [[0, 1], [1, 0], [1, -1], [1, 1]]
    IN_ROW = 4

    def __init__(self):
        self.init_masks = []
        self.default_score = self.get_score()
        for j, (h, w) in enumerate(self.SHAPES):
            tmp = 0
            for i in range(w):
                tmp += 1 << (i * h)
            self.init_masks.append((tmp << 2) + j * 2)

    def get_score(self):
        return {
            (0, 2): -0.002,
            (0, 3): -0.05,
            (0, 4): -1,
            (2, 0): 0.002,
            (3, 0): 0.05,
            (4, 0): 1,
        }

    def any_to_mask(self, s, shape):
        if isinstance(s, str):
            s = s.split("\n")
        if isinstance(s, list):
            h, w = self.SHAPES[shape]
            ans = C.init_masks[shape]
            for i in range(w):
                for j in range(h - 1):
                    k = h - 2 - j
                    if s[k + 1][i] == ".":
                        break
                    pos = i * h + j
                    ans = set_mask(
                        ans, pos + 2, pos + 4, 2 if s[k + 1][i] == "1" else 3
                    )
        else:
            ans = s
        return ans

    def mask_decode(self, s):
        return decode_data(s, self.POS_MASK)

    def mask_encode(self, board, shape, low, player_id):
        boare = set_mask(board, low, low + 2, player_id + 2)
        return encode_data([boare, shape, 1 - player_id], self.POS_MASK)

    def pos_score(self, y, x):
        h, w = self.SHAPES[1]
        yc, xc = abs(h / 2 - y), abs(w / 2 - x)
        c = math.sqrt(yc * yc + xc * xc)
        return c * 0.0000002


C = Constant()
