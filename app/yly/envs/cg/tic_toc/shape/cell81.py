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
        idx = idx // 9
        if idx < len(self.cells) and self.cells[idx].value == 0:
            self.cells[idx].put_all_actions(actions)
        else:
            self.put_all_actions(actions)
        return actions

    def to_str(self, board, info=""):
        self.set_state(board)
        ret = []
        for i in range(11):
            tmp = []
            num2 = 17
            if i % 4 == 3:
                ret.append(["#" if j % 2 == 0 else " " for j in range(num2)])
                continue
            for j in range(num2):
                tmp.append("#" if j % 6 == 5 else " ")
            ret.append(tmp)
        for i in range(C.ALL_SIZE1):
            g = self.cells[i]
            y, x = (g.key // 3) * 4, (g.key % 3) * 3
            if g.value:
                ret[y + 1][(x + 1) * 2] = str(g.value)
                continue
            for j in range(C.ALL_SIZE1):
                c = g.cells[j]
                dy, dx = c.key // 3, c.key % 3
                ret[y + dy][(x + dx) * 2] = " XO"[c.value]
        return info + "\n" + "\n".join(["".join(row) for row in ret])


E = Env(0, None)
