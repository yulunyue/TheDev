from app.yly.algo.cg.cf4.states.base_state import F4State, Action
from app.yly.algo.cg.cf4.states.c4_grid_state import C4GridState
from app.yly.algo.cg.cf4.constant import StateEnum, C
from typing import List, Dict


class F4Action(Action):

    action = None

    def load(self, src, y, x, dst, reward=0):
        self.y, self.x = y, x
        return super().load(src, x, dst, reward)

    def get_line_info(self):
        ret = []
        for k, v in self.dst.state.items():
            v2 = 0 if self.src is None else self.src.state[k]
            if v2 or v:
                ret.append(f"{k[0]}_{k[1]}:{v2}->{v}")
        return "\n".join(ret)

    def get_action_str(self):
        return f"[y={self.y}][x={self.x}][p={S[1-self.dst.player_id]}]\nline_info=\n{self.get_line_info()}\n"

    def get_reward(self, params: StateEnum, **kwargs):
        score = 0
        # for k, v1 in self.dst.state.items():
        #     v2 = 0 if self.src is None else self.src.state[k]
        #     score += params._params[k].get_value() * (v1 - v2)
        return score

    def laod_from_karord(self, board, action):
        self.board = board
        self.action = action
        return self

    def load_from_state(self, state=None):
        self.dst = C4GridState().init_root(state=state)
        return self

    def get_points(self):
        ret = []
        # for k, v1 in self.dst.state.items():
        #     v2 = 0 if self.src is None else self.src.state[k]
        return ret


def get_action(state):
    if isinstance(state, F4Action):
        return state
    return F4Action().load_from_state(state=state)
