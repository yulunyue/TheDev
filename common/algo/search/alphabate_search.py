from common.algo.search.base_search import TreeSearch,State,inf
from typing import List
class ABNode(State):
    alpha=None
    bate=None

class AlphaBateSearch(TreeSearch):
    def search_dp(self, state:ABNode, depth=0, alpha=-inf, bate=inf,**kw) -> None:
        self.state_count+=1
        mvs = state.get_nexts(depth)
        if not mvs:
            return state.calc_value(depth)
        state.alpha, state.bate = alpha, bate
        for action,next_state in mvs.items():
            next_state.value=-self.search_dp(next_state,depth=depth-1,
                                 alpha=-state.bate, bate=-state.alpha)
            if next_state.value >= state.bate:
                state.alpha = state.bate
                state.best_action=action
                break
            if next_state.value > state.alpha:
                state.alpha = next_state.value
                state.best_action=action
        return state.alpha