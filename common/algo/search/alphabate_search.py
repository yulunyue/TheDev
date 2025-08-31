from common.algo.search.state import State, inf, Action
from common.algo.search.algo import Algo
from typing import List, Dict
from common.util.export import logger, defaultdict


class AlphaBateSearch(Algo):
    AB_TYPE = "alphabate"
    AB_MUCH = "abmuch"

    def load(self, max_depth, search_type="", **kw):
        self.max_depth = max_depth
        self.search_type = search_type
        return super().load(**kw)

    def search_ab(
        self,
        state: State,
        actions: List[Action],
        depth=0,
        alpha=-inf,
        bate=inf,
        player_id=None,
        **kw,
    ) -> None:
        if depth == self.max_depth or state.get_done():
            return self.get_depth_reward(
                state,
                depth=depth,
                player_id=player_id,
                params=self.params,
                actions=actions,
            )
        mvs: List[Action] = state.get_sort_actions(depth=depth)
        if not mvs:
            return self.get_depth_reward(
                state,
                depth=depth,
                player_id=player_id,
                params=self.params,
                actions=actions,
            )
        for a in mvs:
            reward = -self.search_ab(
                a.dst,
                actions + [a],
                depth=depth + 1,
                alpha=-bate,
                bate=-alpha,
                player_id=player_id,
            )
            if reward >= bate:
                state.sort_reward = alpha = bate
                state.set_best_action(a)
                break
            if reward > alpha:
                state.sort_reward = alpha = reward
                state.set_best_action(a)
        return alpha

    def get_depth_reward(self, s: State, depth: int, actions: List[Action], **kw):
        return s.get_depth_reward(depth, actions=actions, params=self.params)

    def search_dfs(
        self, state: State, actions: List[Action], depth=0, player_id=None, **kw
    ):
        if depth == self.max_depth or state.get_done():
            return self.get_depth_reward(
                state,
                depth=depth,
                player_id=player_id,
                params=self.params,
                actions=actions,
            )
        mvs: List[Action] = state.get_sort_actions(depth=depth)
        if not mvs:
            return self.get_depth_reward(
                state,
                depth=depth,
                player_id=player_id,
                params=self.params,
                actions=actions,
            )
        best_reward = -inf
        for a in mvs:
            reward = -self.search_dfs(
                a.dst, actions=actions + [a], depth=depth + 1, player_id=player_id
            )
            if reward > best_reward:
                state.set_best_action(a)
                best_reward = reward
        return best_reward

    def seach_ab_much(self, state: State):
        max_depth = self.max_depth + 1
        for depth in range(1, max_depth):
            self.max_depth = depth
            self.search_ab(state, depth=0)

    def search_main(self, state: State, **kw):
        if self.search_type == AlphaBateSearch.AB_TYPE:
            return self.search_ab(state, [], depth=0, player_id=state.player_id, **kw)
        return self.search_dfs(state, [], depth=0, player_id=state.player_id, **kw)


class AbDev(AlphaBateSearch):
    def get_depth_reward(self, s, depth, actions, **kw):
        self.state_num += 1
        return super().get_depth_reward(s, depth, actions, **kw)

    def search(self, state):
        self.state_num = 0
        return super().search(state)
