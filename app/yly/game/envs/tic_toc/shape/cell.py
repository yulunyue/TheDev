from app.yly.game.envs.tic_toc.constant import C
from typing import List, Dict
from .line import Line, LINES


class Cell:
    def __init__(self, key):
        self.key = key
        self.value = self.state = 0
        self.p_lines: List[Line] = []

    def set_state(self, state):
        if state == self.state:
            return self
        for l in self.p_lines:
            l.change(self.state, state)
        self.state = state
        return self


class Cell9(Cell):
    MASK_NUM = 2
    MASK = 3
    CLS_TYPE = Cell

    def __init__(self, pos):
        super().__init__(pos)

        self.cells: List[Cell] = []
        for i in range(C.ALL_SIZE1):
            self.cells.append(self.__class__.CLS_TYPE(i))
        self.c_lines = []
        for a, b, c in LINES:
            ln = Line(self, self.cells[a], self.cells[b], self.cells[c])
            self.c_lines.append(ln)

        self.reset()

    def reset(self):
        self.ct = [[0] * 4 for _ in range(3)]

    def set_state(self, state):
        if self.state == state:
            return self
        self.state = state
        i = 0
        while state:
            self.cells[i].set_state(state & self.MASK)
            state = state >> self.MASK_NUM
            i += 1
        return self

    def add_line_count(self, player_id, src, dst):
        self.ct[player_id][src] -= 1
        self.ct[player_id][dst] += 1
        if self.ct[1][3]:
            self.value = 1
        elif self.ct[2][3]:
            self.value = 2
        else:
            self.value = 0

    def get_actions(self):
        ret = []
        for c in self.cells:
            if c.state:
                continue
            ret.append(c.key * 9 + self.key)
        return ret
