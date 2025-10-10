from typing import List
from common.algo.base.bin_util import decode_data, encode_data


class Constant:
    ROOM_NUM = 12
    SELF_NUM = ROOM_NUM // 2
    POLICY_SIZE = SELF_NUM
    INPUT_SIZE = 6 * 2 * 24 + 2 * 27
    OR_NUM = 4
    MASK_POSS = [5] + [5] * ROOM_NUM
    ALL_SCORE = OR_NUM * ROOM_NUM
    WIN_SCORE = ALL_SCORE // 2 + 1
    MAX_ROUND = 200
    K_LEARNING_RATE = 0.001
    K_MOMENTUM = 0.87  # https://distill.pub/2017/momentum/

    def __init__(self):
        self.INIT_MASK = self.encode_data(0, 0, [self.OR_NUM] * self.ROOM_NUM)

    def encode_data(self, rd, score, boards):
        return encode_data([rd, score] + boards, self.MASK_POSS)

    def decode_data(self, state) -> List[int]:
        return decode_data(state, self.MASK_POSS)

    def get_cases(self):
        return {}


C = Constant()
