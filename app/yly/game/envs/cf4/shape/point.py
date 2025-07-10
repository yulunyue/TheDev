from common.util.export import List, Dict
from app.yly.game.envs.cf4.model.constant import C


class Point:
    def __init__(self, g, y, x):
        from app.yly.game.envs.cf4.shape.grid import Grid

        self.g: Grid = g
        self.y = y
        self.x = x
        self.value = 2
        from app.yly.game.envs.cf4.shape.line import Line

        self.lines: Dict[int, Line] = {}

    def set_value(self, value):
        if self.value == value:
            return
        last_value, self.value = self.value, value
        for (dri, pos_idx), ln in self.lines.items():
            ln.change_value(self, pos_idx, last_value, value)

        return self

    def __repr__(self):
        return f"{self.x}{self.y}"
