from common.algo.export import Action
from app.yly.algo.cg.cf4.cf4state import F4State
from app.yly.algo.cg.cf4.constant import StateEnum, C, S
from typing import List, Dict


class F4Action(Action):

    y = None
    x = None
    dst: F4State
    src: F4State

    def __init__(self, src=None, y=None, x=None, dst=None):
        self.y, self.x = y, x
        super().__init__(src, x, dst)

    def get_action_str(self):
        return f"[y={self.y}][x={self.x}][p={S[self.src.player_id]}]"

    def get_reward(self, params, **kwargs):
        reward, c = 0, 1
        for i, v in enumerate(self.dst.points[::-1]):
            reward += v * c
            c *= 10
        return -reward

    def laod_from_karord(self, board, action):
        self.board = board
        self.action = action
        return self

    def load_from_state(self, state=None):
        self.dst = F4State().init_root(state=state)
        return self

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
