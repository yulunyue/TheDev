from app.yly.game.envs.tic_toc.shape.cell import Cell, Cell9
from app.yly.game.envs.tic_toc.shape.line import Line, LINES
from app.yly.game.envs.tic_toc.constant import C
from typing import List


class Env(Cell9):
    MASK_NUM = 18
    MASK = (1 << MASK_NUM) - 1
    cells: List[Cell9]
    CLS_TYPE = Cell9

    def get_actions(self, last_pos: int):
        y, x = last_pos // 9, last_pos % 9
        idx = y * 2 + x
        if idx < len(self.cells) and self.cells[idx].value == 0:
            actions = self.cells[idx].get_actions()
            if actions:
                return actions
        actions = []
        for c in self.cells:
            if c.value:
                continue
            actions.extend(c.get_actions())
        return actions

    def to_str(self, board):
        self.set_state(board)
        ret = [""]
        for i in range(C.ALL_SIZE1):
            tmp = [f"{i}"]
            for j in range(C.ALL_SIZE1):
                tmp.append("#OX"[self.cells[i].cells[j].state])
            ret.append(" ".join(tmp))
        ret.append("  " + " ".join([str(i) for i in range(C.ALL_SIZE1)]))
        return "\n".join(ret)


E = Env(None)
