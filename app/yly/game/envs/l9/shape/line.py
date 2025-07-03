from typing import List
from app.yly.game.envs.l9.shape.chess import Chess


class Line:

    def __init__(self, chesss: List[Chess]) -> None:
        self.chess_array: List[Chess] = chesss
        self.chess_num = 0
        for c in self.chess_array:
            c.lines.append(self)
