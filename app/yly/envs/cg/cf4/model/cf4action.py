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

        s: F4State = F4State.new(self.next_state)
        if s.depth == C.SIZE:
            s.set_done(2)
        if self.scores[self.src.player_id][0]:
            s.set_done(self.src.player_id)
            score += 1
        else:
            sp = C.POS_SCORE[self.action][s.heights[self.action]]
            score += sp * C.POS_SCORE_RADIO
            score += self.calc_score(*self.scores)
        s.set_reward(score if self.src.player_id == 0 else -score)
        s.set_data(action=self.action, scores=self.scores)
        return s

    def calc_score(self, scores0, scores1):
        c = 0.1
        ret = 0
        for i, v in enumerate(scores0):
            ret += c * v + c * 0.1 * scores1[i]
            c *= 0.01
        return ret
