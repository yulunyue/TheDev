from app.yly.envs.cg.tic_toc.shape.cell9 import Cell, Cell9
from app.yly.envs.cg.tic_toc.shape.line import Line, LINES
from app.yly.envs.cg.tic_toc.constant import C
from typing import List


class Env(Cell9):
    MASK_NUM = 18
    CLS_TYPE = Cell9
    NUM_ALL = 81
    cells:List[Cell9]
    def set_cell_state(self, c:Cell9, value):
        v = c.set_state(value).get_value()
        return super().set_cell_state(c, v)




E = Env(0)
