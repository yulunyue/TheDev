from typing import List
from app.yly.envs.cg.l9.shape.chess import Chess


class Line:

    def __init__(self, chesss: List[Chess]) -> None:
        self.chess_array: List[Chess] = chesss
        for i, c in enumerate(self.chess_array):
            c.lines.append(self)
            if i > 0:
                lc = self.chess_array[i - 1]
                lc.nexts.append(c)
                c.nexts.append(lc)
        self.reset()

    def reset(self):
        self.chess_num = 0
        return self
