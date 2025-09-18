from common.algo.export import Action

from .constant import C
from typing import List, Dict


class F4Action(Action):
    def __init__(self, src, action, state, scores):
        super().__init__(src, action)
        self.next_state = state
        self.scores = scores

    def get_dst(self):
        from .cf4state import F4State

        score = 0
        c = 1 if self.src.player_id == 0 else -1
        s: F4State = F4State.new(self.next_state)
        if s.depth == C.SIZE:
            s.set_done(2)
        if self.scores[self.src.player_id][0]:
            s.set_done(self.src.player_id)
            score += c
        else:
            sp = c * C.POS_SCORE[self.action][s.heights[self.action]]
            score += sp * C.POS_SCORE_RADIO  # action reward  累加问题
        s.set_reward(score)
        return s
