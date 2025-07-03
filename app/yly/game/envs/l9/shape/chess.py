from typing import List


class Chess:

    def __init__(self, key, name) -> None:
        self.key = key
        self.name = name
        self.player_id = 0
        self.in_line = 0
        from app.yly.game.envs.l9.shape.line import Line

        self.lines: List[Line] = []

    def get_pos(self):
        y = ord(self.name[0]) - ord("A")
        x = int(self.name[1]) - 1
        return y, x
