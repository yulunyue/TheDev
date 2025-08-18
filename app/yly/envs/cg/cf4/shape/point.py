from common.util.export import List, Dict
from ..model.constant import C


class Point:
    def __init__(self, g, y, x):
        from ..shape.grid import Grid

        self.g: Grid = g
        self.y = y
        self.x = x
        self.value = 2
        from ..shape.line import Line

        self.lines: Dict[int, Line] = {}

    def set_value(self, value):
        if self.value == value:
            return
        last_value, self.value = self.value, value
        for (dri, pos_idx), ln in self.lines.items():
            if value == 2:
                ln.change_value(self, pos_idx, last_value, -1)
            else:
                if last_value != 2:
                    ln.change_value(self, pos_idx, last_value, -1)
                ln.change_value(self, pos_idx, value, 1)

        return self

    def __repr__(self):
        return f"{self.x}{self.y}"
