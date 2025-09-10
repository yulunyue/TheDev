from .cf4action import F4Action
from .constant import C
from ..shape.grid import Grid
from common.algo.search.state import State, MctsState
from typing import Dict


class F4State(MctsState):
    STATE_STORE: Dict[int, "F4State"] = dict()

    def __init__(self, state):
        self.board, self.shape, player_id = C.mask_decode(state)
        self.g = Grid.new(self.shape)
        self.done, self.actions_state = self.g.set_board(self.board, player_id)

        self.msgs = []
        self.calc_score(self.g.line_ct)
        super().__init__(state, player_id=player_id)

    def calc_score(self, ct: dict):
        self.reward = self.g.pos_score[0] - self.g.pos_score[1]
        self.ct = dict()
        for k, v in ct.items():
            self.ct[f"k{k[0]}{k[1]}"] = v
            self.reward += C.default_score[k] * v
            self.msgs.append(f"k{k[0]}{k[1]}: {v}")
        self.msgs.append("reward:%.5f" % self.reward)
        self.ct["reward"] = self.reward

    def make_actions(self, *args, **kw) -> Dict[str, F4Action]:
        actions = dict()
        for k, v in self.actions_state.items():
            actions[k] = F4Action(self, k, F4State.new(v))

        return actions

    def to_str(self):
        self.g.set_board(self.board, self.player_id)
        return self.g.to_str() + "\n" + "\n".join(self.msgs)

    def get_data(self):
        return self.ct

    def get_action(self, actions):
        if isinstance(actions, str):
            actions = int(actions)
        return super().get_action(actions)
