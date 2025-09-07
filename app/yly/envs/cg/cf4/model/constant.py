from common.algo.base.bin_util import decode_data, encode_data, set_mask


class Constant:
    SHAPES = [[7, 7], [8, 9]]
    POS_MASK = [1, 1]
    DR = [[0, 1], [1, 0], [1, -1], [1, 1]]
    IN_ROW = 4
    CASES = {74076337003370644495: 3}

    def __init__(self):
        self.init_masks = []
        for j, (h, w) in enumerate(self.SHAPES):
            tmp = 0
            for i in range(w):
                tmp += 1 << (i * h)
            self.init_masks.append((tmp << 2) + j * 2)

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


C = Constant()
