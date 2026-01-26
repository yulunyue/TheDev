from .abstate import AbState
from .action import Action
from common.util.export import math, dict_to_str


class MctsState(AbState):
    has_visited = False
    dst: "MctsState"
    n_visits = None

    def load_mcts(self, p_action: "Action" = None):
        self.n_visits = 0
        self.u = 0
        self.q = 0
        self.p_action: Action = p_action
        self.p: MctsState = p_action.src if p_action else None

        return self

    def mcts_update(self, leaf_value):
        if self.p:
            c = -1 if self.mode == self.MAN2 else 1
            self.p.mcts_update(c * leaf_value)
        self.n_visits += 1
        self.q += 1.0 * (leaf_value - self.q) / self.n_visits

    def calc_uct_value(self, exploration_param):
        self.u = exploration_param * math.sqrt(self.p.n_visits / (self.n_visits + 1))
        return self.q + self.u

    def expand(self):
        self.has_visited = True
        for d in self.get_sort_actions():
            d.do().dst.load_mcts(d)
            d.undo()
        return self

    def show_titles(self):
        ret = self.to_json()
        if self.n_visits is not None:
            ret.update(n=self.n_visits, u=self.u, q=self.q)
        return dict_to_str(**ret)
