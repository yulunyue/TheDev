from app.yly.game.envs.tic_toc.constant import C, logger
from common.util.export import List, Dict
from .line import Line, LINES


class Cell:
    def __init__(self, key, p):
        self.key = key
        self.p: Cell9 = p
        self.value = 0
        self.p_lines: List[Line] = []

    def set_state(self, value):
        return self.set_value(value)

    def set_value(self, value):
        if self.value == value:
            return self
        if self.p:
            self.p.value_change(self, value)
            for l in self.p_lines:
                l.change(self.value, value)
        self.value = value
        return self

    def put_all_actions(self, actions: List):
        actions.append(dict(pos=self.key * 9 + self.p.key))


class Cell9(Cell):
    MASK_NUM = 2
    MASK = 3
    CLS_TYPE = Cell

    def __init__(self, pos, p):
        super().__init__(pos, p)
        self.state = 0
        self.cells: List[Cell] = []
        self.value = 0
        self.ct0 = 9
        self.cell_map: List[Dict[int, Cell9]] = [dict(), dict(), dict(), dict()]
        for i in range(C.ALL_SIZE1):
            c = self.__class__.CLS_TYPE(i, self)
            self.cells.append(c)
            self.cell_map[0][c.key] = c
        self.c_lines = []
        for a, b, c in LINES:
            ln = Line(self, self.cells[a], self.cells[b], self.cells[c])
            self.c_lines.append(ln)
        self.ct = [[0] * 4 for _ in range(4)]

    def set_state(self, state):
        if self.state == state:
            return self
        self.state = state
        for i in range(len(self.cells)):
            self.cells[i].set_state(state & self.MASK)
            state = state >> self.MASK_NUM

        return self

    def value_change(self, s: Cell, dst):
        if dst == 0:
            self.ct0 += 1
        if s.value == 0:
            self.ct0 -= 1
        c = self.cell_map[s.value].pop(s.key)
        self.cell_map[dst][s.key] = c

    def add_line_count(self, player_id, src, dst):
        self.ct[player_id][src] -= 1
        self.ct[player_id][dst] += 1
        if self.ct[1][3]:
            self.set_value(1)
        elif self.ct[2][3]:
            self.set_value(2)
        elif self.ct0 == 0:
            self.set_value(3)
        else:
            self.set_value(0)

    def put_all_actions(self, actions):
        cells = list(self.cell_map[0].values())
        for c in cells:
            c.put_all_actions(actions)
