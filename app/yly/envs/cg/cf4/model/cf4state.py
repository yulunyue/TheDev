from .cf4action import F4Action
from .constant import C
from ..shape.grid import Grid
from common.algo.search.state import State
from typing import Dict


class F4State(State):
    STATE_STORE: Dict[int, "F4State"] = dict()
    SCORE = {(0, 2): -0.002, (0, 3): -0.05, (2, 0): 0.002, (3, 0): 0.05}

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
        self.reward = self.g.pos_score[0] - self.g.pos_score[1]
        for k, v in ct.items():
            if v <= 0:
                continue
            if k[0] and k[1]:
                continue
            if k[0] + k[1] == 1:
                continue
            self.reward += self.SCORE[k] * v
            self.msgs.append(f"k{k[0]}{k[1]}: {v}")
        self.msgs.append("reward:%.5f" % self.reward)

    def make_actions(self, *args, **kw) -> Dict[str, F4Action]:
        actions = dict()
        for k, v in self.actions_state.items():
            actions[k] = F4Action(self, k, F4State.new(v))

        return actions

    def to_str(self):
        self.g.set_board(self.board, self.player_id)
        return self.g.to_str() + "\n" + "\n".join(self.msgs)

    def get_action(self, actions):
        if isinstance(actions, str):
            actions = int(actions)
        return super().get_action(actions)
