from .point import Point
from ..model.constant import C
from common.util.export import List, Dict


class Column:
    def __init__(self, p, idx, height):
        from .grid import Grid

        self.p: Grid = p
        self.idx = idx
        self.height = height
        self.mask = (1 << height) - 1
        self.mask_pos = [(1 << i) - 1 for i in range(height)]
        self.state = -1
        self.pts: List[Point] = [Point(p, i, idx) for i in range(height)]
        self.top = 0
        self.pos_score = [C.pos_score(i, idx) for i in range(height)]

    def set_state(self, state: int):
        if self.state == state:
            return
        self.player_pos_score = [0, 0]
        self.state = state
        self.top = state.bit_length() - 1
        for i in range(self.height):
            if i < self.top:
                self.pts[i].set_value(state & 1)
                self.player_pos_score[state & 1] += self.pos_score[i]
            else:
                self.pts[i].set_value(2)
            state = state >> 1
        return self
