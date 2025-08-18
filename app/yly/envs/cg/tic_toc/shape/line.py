from ..constant import C

LINES = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]
from typing import List, Dict


class Line:
    def __init__(self, shap1, shape2, shape3):
        from app.yly.envs.cg.tic_toc.shape.cell import Cell

        self.shapes: List[Cell] = [shap1, shape2, shape3]
        for s in self.shapes:
            s.p_lines.append(self)
        self.nums = [3, 0, 0]

    def get_state(self):
        if self.nums[1] and self.nums[2] == 0:
            return self.nums[1], 0
        if self.nums[2] and self.nums[1] == 0:
            return 0, self.nums[2]
        return 0, 0

    def change(self, f, t):
        last_state = self.get_state()
        self.nums[f] -= 1
        self.nums[t] += 1
        return last_state, self.get_state()
