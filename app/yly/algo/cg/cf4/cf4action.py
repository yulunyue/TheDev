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
        point_info = C.get_point_dr(
            self.src.line_state, self.y, self.x, self.src.player_id
        )
        point_info = C.extend_first_action_scroe(point_info, self.x)
        return C.calc_point_value(point_info)

    def get_reward_by_c4(self):
        point_info, ptsrc = C.get_c4_points(
            self.src.line_state, self.y, self.x, self.src.player_id
        )
        return C.extend_first_action_scroe(point_info, self.x), ptsrc
