from .cf4action import F4Action
from .constant import C
from ..shape.grid import Grid
from common.algo.search.state import State
from typing import Dict


class F4State(State):
    STATE_STORE: Dict[int, "F4State"] = dict()

    def __init__(self, state):
        self.board, self.shape, player_id = C.mask_decode(state)
        self.g = Grid.new(self.shape)
        super().__init__(state, player_id=player_id, depth=0)

    @classmethod
    def new_state(cls, state=None):
        if state is None:
            state = C.init_masks[C.GRID_ENV]
        if state not in F4State.STATE_STORE:
            F4State.STATE_STORE[state] = F4State(state).load()
        return F4State.STATE_STORE[state]

    def load(self):
        self.g.set_board(self.board)
        self.set_done(self.g.done)
        self.set_data(line_ct=dict(self.g.line_ct))
        return self

    def get_done(self):
        self.load()
        return self.done

    def get_player_actions(self, player_id) -> Dict[str, F4Action]:
        actions = dict()
        if not self.get_done():
            action_array = self.g.get_actions(player_id)
            for a in action_array:
                actions[a["action"]] = F4Action(
                    self, a["action"], F4State.new_state(a["mask"])
                )
            if not action_array:
                self.set_done(2)
        return actions

    def get_actions(self, **kw):
        if self.actions is not None:
            return self.actions
        self.actions = self.get_player_actions(self.player_id)
        return self.actions

    def get_reward(self, **kw):
        return 0

    def to_str(self):
        self.load()
        return self.g.to_str()
