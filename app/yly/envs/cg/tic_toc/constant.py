from common.algo.base.bin_util import encode_data, decode_data, set_mask
from common.util.export import List, Dict
from common.algo.search.param import Param, Params





class TcEnum(Params):
    PLAYER2_3 = Param((0, 3), 100)
    PLAYER1_3 = Param((3, 0), -100)
    PLAYER2_2 = Param((0, 2), 10)
    PLAYER1_2 = Param((2, 0), -10)
    PLAYER2_1 = Param((0, 1), 1)
    PLAYER1_1 = Param((1, 0), -1)
    NULL_SATTE = Param((0, 0), 0)


class Constant:
    ROW_SIZE = 3
    COL_SIZE = 3
    ALL_SIZE1 = ROW_SIZE * COL_SIZE
    ALL_SIZE2 = ALL_SIZE1 * ALL_SIZE1
    POS_MASK_NUM = 7
    INIT_STATE81 = 81
    VIEW_STR = [". ", "X ", "O "]

    PLAYER_NULL = 0
    PLAYER_FIRST = 1
    PLAYER_SECOND = 2
    INIT_STATE = 0
    def __init__(self):
        self.STATE_KEYS = [[1<<(2*i),2<<(2*i)] for i in range(81)]

    def decode_state(self, v):
        return decode_data(v, [self.POS_MASK_NUM])

    def encode_state(self, board, player_id, pos):
        board = set_mask(board, pos * 2, pos * 2 + 2, player_id+1)
        return encode_data([board, pos], [self.POS_MASK_NUM])

    def op_pos(self, y, x):
        y1, y2 = y // 3, y % 3
        x1, x2 = x // 3, x % 3
        return (y2 * 3 + x2) * 9 + (y1 * 3 + x1)


    def pos_op(self,pos):
        pos2, pos1 = pos // 9, pos % 9
        _, pos2x = pos2 // 3, pos2 % 3
        _, pos1x = pos1 // 3, pos1 % 3
        return pos2x*2+pos1x
    def get_except_wrong(self):
        pass


C = Constant()
