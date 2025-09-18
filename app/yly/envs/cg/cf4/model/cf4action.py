from common.algo.export import Action

from .constant import C
from typing import List, Dict


class F4Action(Action):
    def __init__(self, src, action, state, scores):
        super().__init__(src, action)
        self.next_state = state
        self.scores: List[List[int]] = scores

    def get_dst(self):
        from .cf4state import F4State

        if self.dst is not None:
            return self.dst
        score = 0

        self.dst: F4State = F4State.new(self.next_state)
        if self.dst.depth == C.SIZE:
            self.dst.set_done(2)
        if self.scores[self.src.player_id][0]:
            self.dst.set_done(self.src.player_id)
            score += 1
        else:
            sp = C.POS_SCORE[self.action][self.dst.heights[self.action]]
            score += sp * C.POS_SCORE_RADIO
            depth = self.dst.heights[self.action]
            while depth < C.HEIGHT - 1 and depth < self.dst.heights[self.action] + 1:
                s0, s1 = self.dst.get_point_scores(self.action, depth)
                self.scores[0].extend(s0)
                self.scores[1].extend(s1)
                depth += 1
            score += self.calc_score(*self.scores)
        self.dst.set_reward(score if self.src.player_id == 0 else -score)
        self.dst.set_data(
            action=self.action, score0=self.scores[0], score1=self.scores[1]
        )
        return self.dst

    def calc_score(self, scores0, scores1):
        c = 0.1
        ret = 0
        for i, v in enumerate(scores0):
            ret += c * v + c * 0.1 * scores1[i]
            c *= 0.01
        return ret
