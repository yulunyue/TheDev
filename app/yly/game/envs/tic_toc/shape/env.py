from app.yly.game.envs.tic_toc.shape.cell import Cell, Cell9
from app.yly.game.envs.tic_toc.shape.line import Line, LINES
from app.yly.game.envs.tic_toc.constant import C
from typing import List


class Env(Cell9):
    MASK_NUM = 18
    MASK = (1 << MASK_NUM) - 1
    cells: List[Cell9]
    CLS_TYPE = Cell9

    def get_actions(self, idx: int):
        actions = []
        if idx < len(self.cells) and self.cells[idx].value == 0:
            actions = self.cells[idx].get_actions()
        if not actions:
            for c in self.cells:
                actions.extend(c.get_actions())
        return actions

    def to_str(self, board,info=""):
        self.set_state(board)
        ret = [info]
        s3="*" + "".join([str(i)+('*' if i%3==2 else ' ') for i in range(C.ALL_SIZE1)])
        for i in range(C.ALL_SIZE1):
            tmp = [f"{i}"]
            for j in range(C.ALL_SIZE1):
                p1=(i//3)*3+(j//3)
                p2=(i%3)*3+(j%3)
                s2 = " OX"[self.cells[p1].cells[p2].value]
                s2+=("*" if j%3==2 else " ")
                tmp.append(s2)
            ret.append("".join(tmp))
            if i%3==2:
                ret.append(s3)
        return "\n".join(ret)


E = Env(None)
