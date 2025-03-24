from common.algo.search.state import State, inf,Action
from common.algo.search.algo import Algo
from typing import List


class AlphaBateSearch(Algo):
    def search_main(self, action: Action, depth=0, alpha=-inf, bate=inf, **kw) -> None:
        self.state_count += 1
        mvs:List[Action] = action.dst.get_actions(depth=depth)
        if not mvs:
            return -action.get_reward(depth=depth)
        for a in mvs:
            value = -self.search_main(a, depth=depth - 1, alpha=-bate, bate=-alpha)
            if value >= bate:
                alpha = bate
                action.dst.best_action = a
                break
            if value > alpha:
                alpha = value
                action.dst.best_action = a
        return alpha
