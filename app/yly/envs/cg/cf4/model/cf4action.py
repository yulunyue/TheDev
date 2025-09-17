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

        s = F4State.new(self.next_state)
        if self.scores[self.src.player_id][0]:
            s.set_done(self.src.player_id)
        return s
