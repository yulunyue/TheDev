from common.algo.search.state import State, inf, Action
from common.algo.search.algo import Algo
from typing import List, Dict


class AlphaBateSearch(Algo):
    def load(self, max_depth, use_cache=False):
        self.max_depth = max_depth
        return super().load(use_cache=use_cache)

    def search_dfs(
        self, state: State, action: Action = None, depth=0, alpha=-inf, bate=inf, **kw
    ) -> None:

        self.state_count += 1
        if depth == -1:
            return -action.get_reward(depth=depth, params=self.params)
        mvs: Dict[str, Action] = state.get_actions(depth=depth)
        if not mvs:
            return -action.get_reward(depth=depth, params=self.params)
        for k, a in mvs.items():
            a.reward = -self.search_dfs(
                a.dst, action=a, depth=depth - 1, alpha=-bate, bate=-alpha
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
        return self.search_dfs(state, None, depth=self.max_depth, **kw)


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
