from typing import Dict, List
from common.algo.search.state import State, Action, inf
from common.algo.search.mttsearch import MctsSearchTree, MctsNode
from app.yly.algo.cg.cf4.constant import C, StateEnum, S
from collections import defaultdict
import json


class F4Action(Action):
    def __str__(self):
        return f"<Action key:{self.action}{S[self.dst.moves%2]} reward:{self.reward}>"


class F4State(MctsNode):
    name = "f4state"
    info = ""

    def __init__(self, mask, moves=-1) -> None:
        self.mask = mask
        self.moves = moves
        self.score = 0

        super().__init__()

    def __str__(self):
        return self.to_str()

    def to_str(self):
        ret = [["- "] * C.WIDTH for _ in range(C.HEIGHT)]
        ret.append([f"{i} " for i in range(C.WIDTH)])

        def util(i, j, v):
            ret[C.HEIGHT - i - 1][j] = S[v] + " "

        C.mask_to_grid(self.mask, util)
        for j in range(C.WIDTH):
            for i in range(self.end_pos[j], C.HEIGHT):
                if (i, j) in self.end_pos:
                    ret[C.HEIGHT - i - 1][j] = f"{self.end_pos[i,j]} "

        check_info = C.check_mask(self.mask, [self.line_state, self.state])
        state_info = [""]
        for k, v in self.state.items():
            s, player_id = k
            if s == StateEnum.STATE_NULL:
                continue
            state_info.append(f"{S[player_id]}:{str(s).split('.').pop()}:{v}")
        state_info = "\n  ".join(state_info)
        from common.algo.search.algo import Baoli

        b = Baoli()
        # bv = b.search(self, depth=20, state_max_num=4000)
        return "\n".join(
            ["**" * C.WIDTH]
            + ["".join(v) for v in ret]
            + [
                f"done:{self.done}; score:{self.score}; actions:{len(self.get_actions())}",
                # f"state:{state_info}",
                # f"sear:[{bv}][{b.state_count}],{'%.3f'%b.use_time};",
                f"info:{self.info}; check:{check_info}",
                f"mask:{self.mask};",
            ]
            + [
                "**" * C.WIDTH,
            ]
        )

    @property
    def key(self):
        return str(self.mask)

    def init_root(self):
        if self.mask == C.INIT_MASK:
            self.line_state = [0] * C.line_num
            self.state = defaultdict(int)
            self.end_pos = {x: 0 for x in range(C.WIDTH)}
            # self.pos = [C.HEIGHT + 1] * C.WIDTH
        else:
            self.line_state, self.state, self.end_pos = C.mask_to_line(self.mask)
        return self

    def calc_value(self, tp="", **kw):
        # if tp == "baoli":
        #     if self.done == 1:
        #         return 3
        #     if self.done == 2:
        #         return -2
        #     return self.done
        return self.score if self.moves % 2 == 0 else -self.score

    def calc_uct_value(self, root):
        return self.score if root.moves % 2 == 0 else -self.score

    def get_action(self, col) -> F4Action:
        x = col * (C.HEIGHT + 1)
        mask0 = self.mask >> x
        y = (mask0 & C.MASK_FULL_HEIGHT).bit_length() - 1
        if y == C.HEIGHT:
            return
        moves = self.moves + 1
        if moves % 2 == 1:
            mask0 |= 2 << y
        else:
            mask0 ^= 3 << y
        mask = (mask0 << x) | (self.mask & C.HEIGHT_POS_MASK[col])
        if mask not in STORE_STATE:
            STORE_STATE[mask] = F4State(mask, moves).init_state(col, y, self)
        return F4Action(self, col, STORE_STATE[mask])

    def init_state(self, x, y, p):
        p: F4State = p
        self.end_pos = p.end_pos.copy()
        self.line_state = p.line_state.copy()
        self.state = p.state.copy()
        score, self.done = C.set_pos(
            y, x, self.moves % 2, self.line_state, self.state, self.end_pos
        )
        self.score = p.score + score
        self.end_pos[x] = y + 1
        return self

    def debug(self):
        from common.util.fp import File

        File("data/log/c4.txt").write_file(str(self))

    def get_actions(self, depth=1):
        if depth == 0 or self.done > 0:
            return []
        if self.actions is None:
            actions = []
            flag = True
            for col in C.COLS:
                a = self.get_action(col)
                if a is None:
                    continue
                s = self.end_pos.get((self.end_pos[col], col), 0)
                if s & self.win_done:
                    actions = [a]
                    break
                if s & self.op_done:
                    actions = [a]
                    flag = True
                if flag:
                    actions.append(a)
            self.actions = actions
        return self.actions

    @property
    def win_done(self):
        return 2 if self.moves % 2 else 1

    @property
    def op_done(self):
        return 3 - self.win_done


STORE_STATE: Dict[int, F4State] = dict()
