from common.algo.base.bin_util import encode_data, decode_data, set_mask
from common.util.export import List, Dict
from common.algo.search.param import Param, Params

LINES = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


class Constant:
    ROW_SIZE = 3
    COL_SIZE = 3
    ALL_SIZE3 = ROW_SIZE * COL_SIZE
    ALL_SIZE9 = ALL_SIZE3 * ALL_SIZE3
    POS_MASK_NUM = 7
    INIT_STATE81 = 81
    VIEW_STR = [". ", "X ", "O "]

    PLAYER_NULL = 0
    PLAYER_FIRST = 1
    PLAYER_SECOND = 2
    INIT_STATE = 0

    def __init__(self):
        self.STATE_KEYS = []
        for i in range(self.ALL_SIZE3):
            self.STATE_KEYS.append(3 << i * 2)
        self.lines: List[List[int]] = []
        for player_id in range(1, 3):
            lns = []
            for l, m, r in LINES:
                v = (
                    (player_id << (l * 2))
                    | (player_id << (m * 2))
                    | (player_id << (r * 2))
                )
                lns.append(v)
            self.lines.append(lns)

    def decode_state(self, v):
        return decode_data(v, [self.POS_MASK_NUM])

    def encode_state(self, board, player_id, pos):
        board = set_mask(board, pos * 2, pos * 2 + 2, player_id + 1)
        return encode_data([board, pos], [self.POS_MASK_NUM])

    def op_pos(self, y, x):
        y1, y2 = y // 3, y % 3
        x1, x2 = x // 3, x % 3
        return (y2 * 3 + x2) * 9 + (y1 * 3 + x1)

    def pos_op(self, pos):
        pos2, pos1 = pos // 9, pos % 9
        _, pos2x = pos2 // 3, pos2 % 3
        _, pos1x = pos1 // 3, pos1 % 3
        return pos2x * 2 + pos1x

    def get_except_wrong(self):
        pass


C = Constant()
