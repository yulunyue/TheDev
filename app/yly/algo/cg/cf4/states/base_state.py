from typing import Dict, List
from common.algo.search.state import State, Action, inf
from app.yly.algo.cg.cf4.constant import C


class F4State(State):

    def __init__(self):
        super().__init__(0, 0)

    def init_root(self, state=None):
        self.state = state
        self.load_root()
        return self

    def load_root(self):
        pass

    def get_actions_all(self):
        return range(C.WIDTH)
