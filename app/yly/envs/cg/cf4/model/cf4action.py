from common.algo.export import Action

from .constant import C
from typing import List, Dict


class F4Action(Action):

    def get_dst2(self):
        from .cf4state import F4State

        if self.dst is not None:
            return self.dst
        score = 0

        self.dst: F4State = F4State.new(self.next_state)
        if self.dst.depth == C.SIZE:
            self.dst.set_done(2)
        if self.scores[self.src.player_id][0]:
            self.dst.set_done(self.src.player_id)
            score = 1
        elif self.scores[self.dst.player_id][0]:
            score = 0.9
        else:
            sp = C.POS_SCORE[self.action][self.dst.heights[self.action]]
            score += sp * C.POS_SCORE_RADIO
            depth = self.dst.heights[self.action]
            scores = self.scores[0][1:] + self.scores[1][1:]
            while depth < C.HEIGHT - 1 and depth < self.dst.heights[self.action] + 2:
                s0, s1 = self.dst.get_point_scores(self.action, depth)
                scores.extend(s0)
                scores.extend(s1)
                depth += 1
            score += self.calc_score(scores)
            self.dst.set_data(
                action=self.action,
                scores=scores,
            )
        self.dst.set_reward(score if self.src.player_id == 0 else -score)
        return self.dst
