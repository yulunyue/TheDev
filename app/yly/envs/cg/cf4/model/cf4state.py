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
        self.done, self.actions_state = self.g.set_board(self.board, player_id)

        self.msgs = []
        if self.done == 0:
            self.reward = 1
        elif self.done == 1:
            self.reward = -1
        else:
            self.calc_score(self.g.line_ct)
        super().__init__(state, player_id=player_id)

    def calc_score(self, ct: dict):
        self.reward = 0
        for k, v in ct.items():
            if v <= 0:
                continue
            if k[0] and k[1]:
                continue
            self.msgs.append(f"k{k[0]}{k[1]}: {v}")

    def make_actions(self, *args, **kw) -> Dict[str, F4Action]:
        actions = dict()
        for k, v in self.actions_state.items():
            actions[k] = F4Action(self, k, F4State.new(v))

        return actions

    def to_str(self):
        self.g.set_board(self.board, self.player_id)
        return self.g.to_str() + "\n" + "\n".join(self.msgs)

    def get_data(self):
        return super().get_data()

    def get_action(self, actions):
        return super().get_action(int(actions))
