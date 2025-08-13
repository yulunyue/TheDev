from .cell import Cell
from .line import Line, LINES
from ..constant import C, TcEnum
from common.util.export import List, Dict, defaultdict


class Cell9(Cell):
    MASK_NUM = 2
    MASK = (1 << MASK_NUM) - 1
    CLS_TYPE = Cell

    def __init__(self):
        self.state = 0
        self.cells: List[Cell] = []
        self.ct_num = [9, 0, 0]
        self.state_count = {}
        for i in range(4):
            self.state_count[0, i] = 0
            self.state_count[i, 0] = 0
        self.cell_map: List[Dict[int, Cell9]] = [dict(), dict(), dict()]
        for i in range(C.ALL_SIZE1):
            c = self.__class__.CLS_TYPE().set_key(i)
            self.cells.append(c)
            self.cell_map[0][c.key] = c
        self.c_lines = []
        for a, b, c in LINES:
            ln = Line(self.cells[a], self.cells[b], self.cells[c])
            self.c_lines.append(ln)
        # self.ct = [[0] * 4 for _ in range(4)]

    def set_state(self, state):
        if self.state == state:
            return self
        self.state = state
        for i in range(len(self.cells)):
            self.set_cell_state(self.cells[i], state & self.MASK)
            state = state >> self.MASK_NUM
        return self

    def get_state(self, c: Cell, player_id):
        return self.state | (player_id << (c.key * 2))

    def set_cell_state(self, c: Cell, value):
        if c.value == value:
            return
        for l in c.p_lines:
            state1, state2 = l.change(c.value, value)
            self.state_count[state1] -= 1
            self.state_count[state2] += 1
        self.ct_num[c.value] -= 1
        self.ct_num[value] += 1
        self.cell_map[c.value].pop(c.key)
        self.cell_map[value][c.key] = c
        c.value = value

    def get_done(self):
        if self.state_count[TcEnum.PLAYER1_3.key]:
            return 1
        if self.state_count[TcEnum.PLAYER2_3.key]:
            return 2
        if self.ct_num[1] + self.ct_num[2] == 9:
            return 3
        return 0
