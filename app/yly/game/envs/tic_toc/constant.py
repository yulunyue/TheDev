from common.algo.base.bin_util import encode_data, decode_data, set_mask


class Constant:
    ROW_SIZE = 3
    COL_SIZE = 3
    ALL_SIZE1 = ROW_SIZE * COL_SIZE
    ALL_SIZE2 = ALL_SIZE1 * ALL_SIZE1

    INIT_SATTE = 10 + (1 << 4)

    MAX_SCORE = 1000

    def decode_state(self, v):
        return decode_data(v, [2, 4])

    def encode_state(self, board, player_id, pos1, pos2):
        if pos2 < C.INIT_SATTE:
            pos = pos1 * 9 + pos2
            board = set_mask(board, pos * 2, pos * 2 + 2, player_id)
        return encode_data([board, 3 - player_id, pos2], [2, 4])


C = Constant()
