from common.algo.search.state import State, inf, Action
from common.algo.search.algo import Algo
from typing import List, Dict
from common.util.export import logger, defaultdict


class AlphaBateSearch(Algo):
    AB_TYPE = "alphabate"

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
            self.state_num += 1
            return self.get_depth_reward(
                state,
                depth=depth,
                player_id=player_id,
                params=self.params,
                actions=actions,
            )
        mvs: Dict[str, Action] = state.get_actions(depth=depth)
        if not mvs:
            self.state_num += 1
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
                state.set_best_action(a)
                break
            if reward > alpha:
                alpha = reward
                state.set_best_action(a)
        return alpha

    def get_depth_reward(self, s: State, depth: int, actions: List[Action], **kw):
        r = s.get_reward(actions, params=self.params)
        return -r if depth % 2 == 1 else r

    def search_dfs(
        self, state: State, actions: List[Action], depth=0, player_id=None, **kw
    ):
        if depth == self.max_depth or state.get_done():
            self.state_num += 1
            return self.get_depth_reward(
                state,
                depth=depth,
                player_id=player_id,
                params=self.params,
                actions=actions,
            )
        mvs: Dict[str, Action] = state.get_actions(depth=depth)
        if not mvs:
            self.state_num += 1
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
                state.set_best_action(a)
                best_reward = reward
        return best_reward

    def search_main(self, state: State, **kw):
        if self.search_type == AlphaBateSearch.AB_TYPE:
            return self.search_ab(state, [], depth=0, player_id=state.player_id, **kw)
        return self.search_dfs(state, [], depth=0, player_id=state.player_id, **kw)
