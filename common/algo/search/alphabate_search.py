from common.algo.search.state import State, inf
from common.algo.search.algo import Algo
from typing import List


class AlphaBateSearch(Algo):
    def search_main(self, state: State, depth=0, alpha=-inf, bate=inf, **kw) -> None:
        self.state_count += 1
        mvs = state.get_actions(depth)
        if not mvs:
            return state.calc_value(depth=depth)
        for a in mvs:
            value = -self.search_main(
                a.state, depth=depth - 1, alpha=-bate, bate=-alpha
            )
            if value >= bate:
                alpha = bate
                state.best_action = a
                break
            if value > alpha:
                alpha = value
                state.best_action = a
        return alpha
