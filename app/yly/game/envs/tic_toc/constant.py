from common.algo.base.bin_util import encode_data, decode_data, set_mask
from common.util.export import List, Dict, get_log

logger = get_log("tic_toc")


class SC:
    SC1 = 7592961601693925925382490737438186337788543455929


class Constant:
    ROW_SIZE = 3
    COL_SIZE = 3
    ALL_SIZE1 = ROW_SIZE * COL_SIZE
    ALL_SIZE2 = ALL_SIZE1 * ALL_SIZE1
    POS_MASK_NUM = 7
    INIT_SATTE = (1 << POS_MASK_NUM) + 81

    MAX_SCORE = 1000

    def decode_state(self, v):
        return decode_data(v, [2, self.POS_MASK_NUM])

    def encode_state(self, board, player_id, pos):
        if pos < 81:
            y, x = pos // 9, pos % 9
            pos1 = x * 9 + y
            board = set_mask(board, pos1 * 2, pos1 * 2 + 2, player_id)
            return encode_data([board, 3 - player_id, pos], [2, self.POS_MASK_NUM])

    def op_pos(self, y, x):
        y1, y2 = y // 3, y % 3
        x1, x2 = x // 3, x % 3
        return (y1 * 3 + x1) + y2 * 3 + x2

    def pos_op(self, pos):
        y, x = pos // 9, pos % 9
        y1, x1, y2, x2 = (
            y // 3,
            y % 3,
            x // 3,
            x % 3,
        )
        return y1 * 3 + y2, x1 * 3 + x2

    def get_except(self):
        return {SC.SC1: 6 * 9 + 1}


C = Constant()
