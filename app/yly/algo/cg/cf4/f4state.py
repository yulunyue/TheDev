from typing import Dict, List
from common.algo.search.state import State, Action, inf
from common.algo.search.mttsearch import MctsSearchTree, MctsNode
from app.yly.algo.cg.cf4.constant import C, StateEnum, S

STORE_STATE: Dict[int, State] = dict()


class F4Action(Action):
    def __str__(self):
        return f"<Action key:{self.key}{S[self.state.moves%2]} reward:{self.reward}>"


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
        return "\n".join(
            ["**" * C.WIDTH]
            + ["".join(v) for v in ret]
            + [
                f"done:{self.done}; score:{'%.4f'%self.score}; actons:{len(self.get_actions())}",
                f"cache_done:{self.get_cache_done()}; info:{self.info}; check:{C.check_mask(self.mask,[self.line_state,self.state])}",
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
            self.state = [[0] * len(StateEnum) for _ in range(2)]
        else:
            self.line_state, self.state = C.mask_to_line(self.mask)
        return self

    def calc_value(self, root=None, **kw):
        if root:
            return self.score if root.moves % 2 == 0 else -self.score
        return self.score if self.moves % 2 == 0 else -self.score

    def get_action(self, col) -> F4Action:
        x = col * (C.HEIGHT + 1)
        mask0 = self.mask>>x
        y = (mask0&C.MASK_FULL_HEIGHT).bit_length()-1
        if y == C.HEIGHT:
            return
        moves = self.moves + 1
        if moves % 2 == 1:
            mask0 |= (2<<y)
        else:
            mask0 ^= (3<<y)
        mask = (mask0<<x) | (self.mask&C.HEIGHT_POS_MASK[col]) 
        if mask not in STORE_STATE:
            STORE_STATE[mask] = F4State(mask, moves).init_state(col, y, self)
        return F4Action(col, STORE_STATE[mask])

    def init_state(self, x, y, p):
        p: F4State = p
        self.line_state = p.line_state.copy()
        self.state = [p.state[0].copy(), p.state[1].copy()]
        score, self.down = C.set_pos(y, x, self.moves % 2, self.line_state, self.state)
        self.score = p.score + score
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
                if a.state.done == a.state.win_done:
                    actions = [a]
                    break
                if a.state.done == -2:
                    actions = [a]
                    flag = False
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
