from common.algo.search.state import State, inf, Action
from common.algo.search.algo import Algo
from typing import List


class AlphaBateSearch(Algo):
    def search_dfs(
        self, action: Action, depth=0, alpha=-inf, bate=inf, budget=0, **kw
    ) -> None:
        # if budget and self.state_count >= budget:
        #     return inf
        self.state_count += 1
        mvs: List[Action] = action.dst.get_actions(depth=depth)
        if not mvs:
            return -action.get_reward(depth=depth)
        for a in mvs:
            a.reward = -self.search_dfs(
                a, depth=depth - 1, alpha=-bate, bate=-alpha, budget=budget
            )
            if a.reward >= bate:
                alpha = bate
                action.dst.best_action = a
                break
            if a.reward > alpha:
                alpha = a.reward
                action.dst.best_action = a
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
