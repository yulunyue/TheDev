from common.algo.search.state import State,inf
from common.algo.search.algo import Algo
from typing import List
class ABNode(State):
    alpha=None
    bate=None

class AlphaBateSearch(Algo):
    def search_main(self, state:ABNode, depth=0, alpha=-inf, bate=inf,**kw) -> None:
        self.state_count+=1
        mvs = state.get_nexts(depth)
        if not mvs:
            return state.calc_value(depth=depth)
        state.alpha, state.bate = alpha, bate
        for a in mvs:
            a.state.value=-self.search_main(a.state,depth=depth-1,
                                 alpha=-state.bate, bate=-state.alpha)
            if a.state.value >= state.bate:
                state.alpha = state.bate
                state.best_action=a
                break
            if a.state.value > state.alpha:
                state.alpha = a.state.value
                state.best_action=a
        return state.alpha