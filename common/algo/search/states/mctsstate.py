from .abstate import AbState
from common.util.export import math


class MctsState(AbState):
    n_visits = None

    def load_mcts(self, p_action: "Action" = None):
        self.n_visits = 0
        self.u = 0
        self.q = 0
        self.p_action: Action = p_action
        self.p: MctsState = p_action.src if p_action else None

    def mcts_update(self, leaf_value):
        if self.p:
            self.p.mcts_update(-leaf_value)
        self.n_visits += 1
        self.q += 1.0 * (leaf_value - self.q) / self.n_visits

    def calc_uct_value(self, exploration_param):
        self.u = exploration_param * math.sqrt(self.p.n_visits / (self.n_visits + 1))
        return self.q + self.u
