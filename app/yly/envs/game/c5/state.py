from common.algo.export import AbState, Action
from .constant import C


class State(AbState):
    def __init__(self, state, player_id=0, depth=0):
        super().__init__(state, player_id, depth)
