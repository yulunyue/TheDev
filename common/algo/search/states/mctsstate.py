from .abstate import AbState
from .action import Action
from common.util.export import math, dict_to_str, inf


class MctsState(AbState):
    has_visited = False
    dst: "MctsState"
    n_visits = q = 0
    u = inf

    def load_mcts(self, p_action: "Action"):
        self.p_action: Action = p_action
        self.n_visits = self.q = 0
        self.u = inf
        self.has_visited = True
        return self

    def expand(self):
        for d in self.get_sort_actions():
            d.dst.has_visited = False
        return self

    def show_titles(self):
        ret = self.to_json()
        if self.has_visited:
            ret.update(n=self.n_visits, u=self.u, q=self.q)
        return dict_to_str(**ret)
