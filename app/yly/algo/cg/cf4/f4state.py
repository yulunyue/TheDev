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
        for j in range(C.WIDTH):
            pos = j * (C.HEIGHT + 1)
            h_mask: int = (self.mask >> pos) & C.MASK_FULL_HEIGHT
            l = h_mask.bit_length() - 1
            for i in range(l):
                k = C.HEIGHT - (l - i)
                if h_mask & (1 << i):
                    ret[k][j] = S[1] + " "
                else:
                    ret[k][j] = S[0] + " "

        return "\n".join(
            ["**" * C.WIDTH]
            + ["".join(v) for v in ret]
            + [
                f"done:{self.done}; score:{'%.4f'%self.score}; actons:{len(self.get_actions())}",
                f"cache_done:{self.get_cache_done()}; info:{self.info}; check:{C.check_mask(self.mask,self.line_state)}",
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
        mask0: int = (self.mask & C.HEIGHT_MASK1[col]) << 1
        # self.info += f"\n{col}\n{bin(mask0)}\n{bin(C.HEIGHT_POS_MASK[col][0])}\n"
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
        return F4Action(col, STORE_STATE[mask])

    def init_state(self, x, y, p):
        p: F4State = p
        self.line_state = p.line_state.copy()
        # self.info += f"{x} {y} {bin(self.line_state[87])}"
        self.state = [p.state[0].copy(), p.state[1].copy()]
        player_id = self.moves % 2
        self.score = p.score
        for line_id, k_id in C.point_line_id[y][x]:

            old_state = self.line_state[line_id]
            if old_state & C.state_pos[k_id][player_id]:
                raise Exception(C.lines[k_id])
            new_state = old_state | C.state_pos[k_id][player_id]
            # p.info += f"{line_id}:{bin(new_state)}\n"
            self.line_state[line_id] = new_state
            new_state_id, new_score = C.scores[player_id][new_state]
            old_state_id, old_score = C.scores[player_id][old_state]
            if old_state_id != new_state_id:
                self.state[player_id][old_state_id] -= 1
                self.state[player_id][new_state_id] += 1
                self.score += (new_score - old_score) * [1, -1][player_id]
            if new_state_id == StateEnum.STATE_40:
                self.score = [1, -1][player_id]
                # p.info += f"[set {self.score}]"
                self.set_done(player_id + 1)
            if new_state_id == StateEnum.STATE_13 and self.done == -1:
                # p.info += "[set -2]"
                self.set_done(-2)
        # if self.score >= 1 or self.score <= -1:
        #     raise Exception(self.score)
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

                # self.info += f"[{a.key} {a.state.done} {self.win_done}]"
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
