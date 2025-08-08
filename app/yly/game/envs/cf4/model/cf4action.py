from common.algo.export import Action

from app.yly.game.envs.cf4.model.constant import C
from typing import List, Dict


class F4Action(Action):

    def __init__(self, src, action, dst):
        from app.yly.game.envs.cf4.model.cf4state import F4State

        self.action = action
        self.src: "F4State" = src
        self.dst: "F4State" = dst

    def get_reward(self, *args, **kw):
        return self.dst.get_reward()
