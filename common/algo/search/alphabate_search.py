from common.algo.search.state import State, inf
from common.algo.search.algo import Algo
from typing import List


class AlphaBateSearch(Algo):
    def search_dfs(
        self, state: State, depth=0, alpha=-inf, bate=inf, budget=0, **kw
    ) -> None:
        # if budget and self.state_count >= budget:
        #     return inf
        self.state_count += 1
        mvs = state.get_actions(depth)
        if not mvs:
            return -state.calc_value(depth=depth)
        for a in mvs:
            a.reward = -self.search_dfs(
                a.dst, depth=depth - 1, alpha=-bate, bate=-alpha, budget=budget
            )
            if a.reward >= bate:
                alpha = bate
                state.best_action = a
                break
            if a.reward > alpha:
                alpha = a.reward
                state.best_action = a
        return alpha

    def search_main(self, state, **kw):
        return self.search_dfs(state, **kw)


class AbSearchIter(AlphaBateSearch):
    def search_main(self, state, depth, budget=0, **kw):
        turn = 1
        while turn <= depth:
            self.search_dfs(state, turn, budget=budget)
            if budget and self.state_count >= budget:
                break
            turn += 1
        return turn

    def search_dfs(self, state: State, depth=0, alpha=-inf, bate=inf, **kw):
        ret = super().search_dfs(state, depth, alpha, bate, **kw)
        if state.actions and len(state.actions) > 1:
            state.actions.sort(key=lambda a: a.reward)
        return ret
