from common.algo.search.state import State, inf, Action
from common.algo.search.algo import Algo
from typing import List, Dict
from common.util.export import logger, defaultdict


class AlphaBateSearch(Algo):
    AB_TYPE = "alphabate"
    SERACH_MAX = "search_max"

    def load(self, max_depth, cache=None, search_type=""):
        self.max_depth = max_depth
        self.search_type = search_type
        return super().load(cache=cache)

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
        mvs: Dict[str, Action] = state.get_actions(depth=depth)
        if not mvs:
            return self.get_depth_reward(
                state,
                depth=depth,
                player_id=player_id,
                params=self.params,
                actions=actions,
            )
        for k, a in mvs.items():
            reward = -self.search_ab(
                a.dst,
                actions + [a],
                depth=depth + 1,
                alpha=-bate,
                bate=-alpha,
                player_id=player_id,
            )
            if reward >= bate:
                alpha = bate
                state.set_best_action(a.set_reward(reward))
                break
            if reward > alpha:
                alpha = reward
                state.set_best_action(a.set_reward(reward))
        return alpha

    def get_depth_reward(self, s: State, depth: int, actions: List[Action], **kw):
        return s.get_self_reward(actions, params=self.params)

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
        mvs: Dict[str, Action] = state.get_actions(depth=depth)
        if not mvs:
            return self.get_depth_reward(
                state,
                depth=depth,
                player_id=player_id,
                params=self.params,
                actions=actions,
            )
        best_reward = -inf
        for k, a in mvs.items():
            reward = -self.search_dfs(
                a.dst, actions=actions + [a], depth=depth + 1, player_id=player_id
            )
            if reward > best_reward:
                state.set_best_action(a.set_reward(reward))
                best_reward = reward
        return best_reward

    def search_max(self, s: State):
        max_action = None
        max_reward = None
        for a in s.get_actions().values():
            reward = s.get_reward(actions=[a])
            if max_reward is None or reward > max_reward:
                max_reward = reward
                max_action = a
        if max_action is not None:
            s.set_best_action(max_action)

    def search_main(self, state: State, **kw):
        if self.search_type == AlphaBateSearch.AB_TYPE:
            return self.search_ab(state, [], depth=0, player_id=state.player_id, **kw)
        elif self.search_type == AlphaBateSearch.SERACH_MAX:
            return self.search_max(state)
        return self.search_dfs(state, [], depth=0, player_id=state.player_id, **kw)
