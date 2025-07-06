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
    def __init__(self, p, shap1, shape2, shape3):
        from app.yly.game.envs.tic_toc.shape.cell import Cell9, Cell

        self.p: Cell9 = p
        self.shapes: List[Cell] = [shap1, shape2, shape3]
        for s in self.shapes:
            s.p_lines.append(self)
        self.nums = [3, 0, 0, 0]

    def change(self, f, t):
        self.p.add_line_count(f, self.nums[f], self.nums[f] - 1)
        self.p.add_line_count(t, self.nums[t], self.nums[t] + 1)
        self.nums[f] -= 1
        self.nums[t] += 1
