from typing import List
from common.algo.base.bin_util import decode_data, encode_data


class Constant:
    ROOM_NUM = 12
    SELF_NUM = ROOM_NUM // 2
    OR_NUM = 4
    MASK_POSS = [5] + [5] * ROOM_NUM
    ALL_SCORE = OR_NUM * ROOM_NUM
    WIN_SCORE = ALL_SCORE  // 2+1
    MAX_ROUND = 200

    def __init__(self):
        self.INIT_MASK = self.encode_data(0, 0, [self.OR_NUM] * self.ROOM_NUM)

    def encode_data(self, rd, score, boards):
        return encode_data([rd, score] + boards, self.MASK_POSS)

    def decode_data(self, state) -> List[int]:
        return decode_data(state, self.MASK_POSS)

    def get_cases(self):
        return {}


C = Constant()
