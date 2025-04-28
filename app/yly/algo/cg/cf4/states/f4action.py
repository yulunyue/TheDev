from app.yly.algo.cg.cf4.states.base_state import Action
from app.yly.algo.cg.cf4.states.c4_grid_state import C4GridState
from app.yly.algo.cg.cf4.constant import StateEnum, C, S
from typing import List, Dict


class F4Action(Action):

    y = None
    x = None

    def __init__(self, src, y, x, dst, reward=0):
        self.y, self.x = y, x
        super().__init__(src, x, dst, reward)

    def get_line_info(self):
        ret = []

        return "\n".join(ret)

    def get_action_str(self):
        return f"[y={self.y}][x={self.x}][p={S[1-self.dst.player_id]}]line_info={self.get_line_info()}"

    def get_reward(self, params: StateEnum, **kwargs):
        score = 0

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

    _debug_file = None

    def debug(self, info=""):
        from common.util.fp import File

        if not F4Action._debug_file:
            fp = File("data/log/c4.txt").write_file("init\n")
            F4Action._debug_file = open(fp.path, "w", encoding="utf-8")
        if info.startswith("msg"):
            F4Action._debug_file.write(f"\n-----{info}----\n")
        else:
            F4Action._debug_file.write(str(self))


def get_action(state):
    if isinstance(state, F4Action):
        return state

    state = C4GridState().init_root(state=state)
    return F4Action(None, None, None, state)
