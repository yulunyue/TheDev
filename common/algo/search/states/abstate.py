from .state import State, inf
from .action import Action


class AbState(State):

    def load_ab(self, search_depth=0, alpha=-inf, bate=inf, p_action=None):
        self.search_depth = search_depth
        self.child_index = 0
        self.alpha = alpha
        self.bate = bate
        self.p_action: Action = p_action
        return self
