from .cell import Cell
from .line import Line, LINES
from ..constant import C, TcEnum
from common.util.export import List, Dict, defaultdict


class Cell9(Cell):
    MASK_NUM = 2
    CLS_TYPE = Cell
    NUM_ALL=9
    @property
    def MASK(self):
        return (1 << self.MASK_NUM) - 1

    def __init__(self,key):
        super().__init__(key)
        self.state = 0
        self.cells: List[Cell] = []
        self.ct_num = [9, 0, 0]
        self.state_count = {}
        for i in range(4):
            self.state_count[0, i] = 0
            self.state_count[i, 0] = 0
        self.cell_map: List[Dict[int, Cell9]] = [dict(), dict(), dict()]
        for i in range(C.ALL_SIZE1):
            c = self.__class__.CLS_TYPE(self.key*9+i)
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
        if self.state_count[TcEnum.PLAYER1_3.key] or self.state_count[TcEnum.PLAYER2_3.key]:
            return True
        if self.ct_num[1] + self.ct_num[2] == self.NUM_ALL:
            return True
        return False
    def get_value(self):
        if self.state_count[TcEnum.PLAYER1_3.key]:
            return 1
        if self.state_count[TcEnum.PLAYER2_3.key]:
            return 2
        return 0
      
    def get_reward(self):
        v = self.get_value()
        if v==1:
            return 1
        if v==2:
            return -1
        return 0