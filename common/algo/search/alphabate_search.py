from common.algo.search.state import State, inf, Action
from common.algo.search.algo import Algo
from typing import List, Dict
from common.util.export import logger


class AlphaBateSearch(Algo):
    def load(self, max_depth, use_cache=False, use_alpha_bate=True):
        self.max_depth = max_depth
        self.use_alpha_bate = use_alpha_bate
        return super().load(use_cache=use_cache)

    def search_ab(
        self,
        state: State,
        action: Action = None,
        depth=0,
        alpha=-inf,
        bate=inf,
        player_id=None,
        **kw
    ) -> None:
        if depth == self.max_depth:
            return state.get_reward(
                depth=depth, params=self.params, player_id=player_id, action=action
            )
        mvs: Dict[str, Action] = state.get_actions(depth=depth)
        if not mvs:
            return state.get_reward(
                depth=depth, params=self.params, player_id=player_id, action=action
            )
        for k, a in mvs.items():
            reward = self.search_ab(
                a.dst,
                action=a,
                depth=depth + 1,
                alpha=-bate,
                bate=-alpha,
                player_id=player_id,
            )
            if reward >= bate:
                alpha = bate
                state.set_best_action(a)
                break
            if reward > alpha:
                alpha = reward
                state.set_best_action(a)
        return alpha

    def search_dfs(
        self, state: State, action: Action = None, depth=0, player_id=None, **kw
    ):
        if depth == self.max_depth:
            return state.get_reward(
                depth=depth, params=self.params, player_id=player_id, action=action
            )
        mvs: Dict[str, Action] = state.get_actions(depth=depth)
        if not mvs:
            return state.get_reward(
                depth=depth, params=self.params, player_id=player_id, action=action
            )
        best_reward = -inf
        for k, a in mvs.items():
            reward = self.search_dfs(a.dst, action=a, depth=depth + 1)
            if reward > best_reward:
                state.set_best_action(a)
                best_reward = reward
        return best_reward

    def search_main(self, state: State, **kw):
        if self.use_alpha_bate:
            return self.search_ab(
                state, action=None, depth=0, player_id=state.player_id, **kw
            )
        return self.search_dfs(
            state, action=None, depth=0, player_id=state.player_id, **kw
        )
