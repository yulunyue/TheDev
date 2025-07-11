from common.algo.base.bin_util import decode_data, encode_data, set_mask


class Constant:
    S1 = """
.......
.......
.......
.......
..222..
..111..
"""
    S2 = """
.......
.......
.......
12.....
12.....
12.....
"""
    S3 = """
.......
.......
.......
..121..
21212..
12121..
"""
    S4 = """
.......
.......
..121..
..122.2
11211.1
2211222
"""
    SHAPES = [[7, 7], [8, 9]]
    DR = [[0, 1], [1, 0], [1, -1], [1, 1]]
    IN_ROW = 4

    def __init__(self):
        self.init_masks = []
        for j, (h, w) in enumerate(self.SHAPES):
            tmp = 0
            for i in range(w):
                tmp += 1 << (i * h)
            self.init_masks.append((tmp << 2) + (j << 1))

    def get_cases(self):
        return {
            self.S1: "1 5\nNONE",
            self.S2: "0\n1",
            self.S3: "3\n4",
            self.S4: "5\n5",
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
        return decode_data(s, [1, 1])

    def mask_encode(self, board, shape, low, player_id):

        return (
            (set_mask(board, low, low + 2, player_id + 2) << 2)
            + (shape << 1)
            + 1
            - player_id
        )


C = Constant()
