from common.algo.search.state import State

from app.yly.envs.cg.tic_toc.shape.cell81 import E, Cell9
from app.yly.envs.cg.tic_toc.constant import C
from app.yly.envs.cg.tic_toc.model.ttaction import TtAction
from typing import List, Dict


class TtState(State):
    def __init__(self, state):
        self.board, self.last_pos = C.decode_state(state)
        E.set_state(self.board)
        depth = E.ct_num[1] + E.ct_num[2]
        self.set_done(E.get_done()).set_reward(E.get_reward())
        super().__init__(state, depth % 2, depth)

    def make_actions(self, depth=1, **kw):
        actions = dict()
        e = E.set_state(self.board)
        idx = C.pos_op(self.last_pos)
        cells: List[Cell9] = []
        if E.cells[idx].get_value() == 0:
            cells.extend(E.cells[idx].cell_map[1 + self.player_id].values())
        else:
            for c in E.cells:
                if c.get_value() == 0:
                    cells.extend(c.cell_map[1 + self.player_id].values())

        for c in cells:
            k = C.encode_state(self.board, self.player_id, c.key)
            ac = TtAction(
                self,
                a["pos"],
                TtState.new_state(k),
            )
            self.actions[ac.action] = ac
        return self.actions

    def get_action(self, a):
        actions = self.get_actions()
        if a in actions:
            return actions[a]
        raise Exception(a, list(actions.keys()))

    def to_str(self):
        return E.to_str(
            self.board,
            f"last_pos:{[self.last_pos%9,self.last_pos//9]}, actions:{len(self.get_actions().keys())}",
        )

    def get_win_player(self):
        if self.done == 1 or self.done == 2:
            return self.done
        return None

    def get_reward(self, player_id, **kwargs):
        value = 0
        done = self.get_done()
        if done == 1:
            value = -C.MAX_SCORE
        elif done == 2:
            value = C.MAX_SCORE
        return value if player_id == done else -value

    def get_done(self):
        if self.done is None:
            self.get_actions()
        return self.done

    def to_str(self):
        E.set_state(self.state)
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
            g = E.cells[i]
            y, x = (g.key // 3) * 4, (g.key % 3) * 3
            #     if g.value: XX#
            #         ret[y + 1][(x + 1) * 2] = str(g.value)
            #         continue
            for j in range(C.ALL_SIZE1):
                c = g.cells[j]
                k = c.key % 9
                dy, dx = k // 3, k % 3
                ret[y + dy][(x + dx) * 2] = " XO"[c.value]
        return "\n".join(["".join(row) for row in ret])
