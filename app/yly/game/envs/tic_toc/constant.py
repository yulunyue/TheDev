from common.algo.base.bin_util import encode_data, decode_data, set_mask


class Constant:
    ROW_SIZE = 3
    COL_SIZE = 3
    ALL_SIZE1 = ROW_SIZE * COL_SIZE
    ALL_SIZE2 = ALL_SIZE1 * ALL_SIZE1

    INIT_SATTE = 90 + (1 << 7)

    def decode_state(self, v):
        return decode_data(v, [2, 7])

    def encode_state(self, board, player_id, last_pos):
        if last_pos < C.INIT_SATTE:
            board = set_mask(board, last_pos * 2, last_pos * 2 + 2, player_id)
        return encode_data([board, 3 - player_id, last_pos], [2, 7])


C = Constant()
