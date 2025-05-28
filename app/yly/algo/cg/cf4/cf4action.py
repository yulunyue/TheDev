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

    def get_reward(self, params=None, **kwargs):
        reward, c = 0, 1
        return -reward

    def get_reward_by_c4(self):
        k = self.y * C.WIDTH + self.x
        return C.get_c4_points(self.dst.line_state, k, self.dst.player_id)
