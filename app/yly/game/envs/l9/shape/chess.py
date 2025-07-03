from typing import List


class Chess:

    def __init__(self, key, idx) -> None:
        self.key = key
        self.mask = 1 << idx
        self.idx = idx
        from app.yly.game.envs.l9.shape.line import Line

        self.lines: List[Line] = []
        self.nexts: List[Chess]=[]
        self.reset()

    def get_pos(self):
        y = ord(self.key[0]) - ord("A")
        x = int(self.key[1]) - 1
        return y, x

    def reset(self):
        self.player_id = 0
        self.in_line = 0
        return self
