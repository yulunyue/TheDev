from common.algo.export import State, Action
from common.util.export import logger
from typing import Dict
import numpy as np
from .constant import C


class CfState(State):
    def __init__(self, state):
        self.y, self.x = state // C.ncol, state % C.ncol
        super().__init__(state)

    def make_actions(self):
        actions = []
        if self.game_over:
            return actions
        for i, (dy, dx) in enumerate(C.ACTIONS):
            reward = -1
            ny, nx = dy + self.y, dx + self.x
            if ny < 0 or nx < 0 or ny >= C.nrow or nx >= C.ncol:
                next_state = self
            else:
                next_state = CfState.new(ny * C.ncol + nx)
            if ny == C.nrow - 1 and nx > 0:
                if nx != C.ncol - 1:
                    reward = -100
                next_state.set_done(True)
            a = Action(self, i, next_state).set_reward(reward)
            actions.append(a)
        return actions

    def bfs(self, max_depth=-2):
        return [d[1] for d in super().bfs(max_depth).values()]
