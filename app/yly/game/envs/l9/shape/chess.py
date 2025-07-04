from typing import List
from ..constant import C


class Chess:

    def __init__(self, key, idx) -> None:
        self.key = key
        self.mask1, self.mask2 = C.get_mask(idx)
        self.idx = idx
        from app.yly.game.envs.l9.shape.line import Line

        self.lines: List[Line] = []
        self.nexts: List[Chess] = []
        self.reset()

    def get_pos(self):
        x = ord(self.key[0]) - ord("A")
        y = int(self.key[1]) - 1
        return y, x

    def reset(self):
        self.player_id = 0
        self.in_line = 0
        return self

    def set_player_id(self, board, player_id):
        if player_id == 3:
            raise Exception("todo")
        self.player_id = player_id
        return (board & self.mask1) | (player_id * self.mask2)
