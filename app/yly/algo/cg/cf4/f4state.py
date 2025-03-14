from typing import Dict, List
from common.algo.search.state import State, Action
from common.algo.search.mttsearch import MctsSearchTree, MctsNode
from app.yly.algo.cg.cf4.constant import C, StateEnum, S

STORE_STATE: Dict[int, State] = dict()


def action_to_str(a: Action):
    s: F4State = a.state
    ret = [["- "] * C.WIDTH for _ in range(C.HEIGHT)]
    ret.append([f"{i} " for i in range(C.WIDTH)])
    for j in range(C.WIDTH):
        pos = j * (C.HEIGHT + 1)
        h_mask: int = (s.mask >> pos) & C.MASK_FULL_HEIGHT
        l = h_mask.bit_length() - 1
        for i in range(l):
            k = C.HEIGHT - (l - i)
            if h_mask & (1 << i):
                ret[k][j] = S[1] + " "
            else:
                ret[k][j] = S[0] + " "
    return "\n".join(
        [f"a:{a.key}{S[s.moves%2]}, done:{s.done} "] + ["".join(v) for v in ret]
    )


class F4State(MctsNode):
    def __init__(self, mask, moves=-1) -> None:
        self.mask = mask
        self.moves = moves
        self.score = 0
        super().__init__()

    @property
    def key(self):
        return self.mask

    def init_root(self):
        self.line_state = [0] * C.line_num
        self.state = [0] * len(StateEnum)
        return self

    def calc_value(self, **kw):
        return self.score if self.moves % 2 == 0 else -self.score

    def get_action(self, col) -> Action:
        mask0: int = (self.mask & C.HEIGHT_MASK1[col]) << 1
        if mask0 & C.HEIGHT_POS_MASK[col][0]:
            return
        mask1 = self.mask & C.HEIGHT_MASK0[col]
        moves = self.moves + 1
        if moves % 2 == 1:
            mask1 |= C.HEIGHT_POS_MASK[col][1]
        else:
            mask1 &= C.HEIGHT_POS_MASK[col][2]
        mask = mask1 | mask0
        if mask not in STORE_STATE:
            STORE_STATE[mask] = F4State(mask, moves).init_state(
                col, mask0.bit_length() - col * (C.HEIGHT + 1) - 2, self
            )
        return Action(col, STORE_STATE[mask])

    def init_state(self, x, y, p):
        p: F4State = p
        self.line_state = p.line_state.copy()
        self.state = p.state.copy()
        for line_id, k_id in C.point_line_id[y][x]:
            old_state = self.line_state[line_id]
            new_state = old_state | C.state_pos[k_id][self.moves % 2]
            self.line_state[line_id] = new_state
            new_state_id, *args = C.scores[self.moves % 2][new_state]
            old_state_id, *args = C.scores[self.moves % 2][old_state]
            if new_state_id == StateEnum.STATE_40:
                return self.set_done((self.moves % 2) + 1)
            if new_state_id == StateEnum.STATE_31:
                return self.set_done(-2)
            self.state[old_state_id] = self.state[old_state_id] - 1
            self.state[new_state_id] = self.state[new_state_id] + 1
        return self

    def score_detail(self):
        return f'a:{str(self.best_action)[0]}{"XO"[self.moves%2]};s:{self.score}'

    def debug(self):
        from common.util.fp import File

        File("data/log/c4.txt").write_file(str(self))

    def get_actions(self, depth=1):
        if depth == 0 or self.done > 0:
            return []
        if self.actions is None:
            actions = []
            flag=True
            for col in C.COLS:
                a = self.get_action(col)
                if a is None:
                    continue
                if a.state.done>0:
                    actions = [a]
                    break
                if a.state.done==-2:
                    actions=[a]
                    flag=False
                if flag:
                    actions.append(a)
            self.actions=actions
        return self.actions
