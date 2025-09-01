from common.algo.search.state import AbState as State, inf, Action
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

    def get_depth_reward(
        self, s: State, depth: int = None, actions: List[Action] = None, **kw
    ):
        return s.get_self_reward(depth=depth, actions=actions, params=self.params)

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

    def search_ab_loop(self, state: State):
        stacks = [state]
        state.depth = 0
        best_action = None
        while stacks:
            cur_node = stacks[-1]
            if cur_node.get_done() or cur_node.depth == self.max_depth:
                cur_node.ab_value = self.get_depth_reward(cur_node)
                stacks.pop()
                continue
            actions = cur_node.get_sort_actions()
            if cur_node.child_index == len(actions):
                stacks.pop()
                if stacks:
                    p = stacks[-1]
                    if p.depth % 2 == 0:
                        if p.ab_value is None or p.ab_value < cur_node.ab_value:
                            p.ab_value = cur_node.ab_value
                        if p.alpha < cur_node.alpha:
                            p.alpha = cur_node.alpha
                    else:
                        if p.ab_value is None or p.ab_value > cur_node.ab_value:
                            p.ab_value = cur_node.ab_value
                        if p.bate > cur_node.bate:
                            p.bate = cur_node.bate
                    if p.alpha >= p.bate:
                        p.child_index = len(actions)
                        if len(state) == 1 and cur_node.ab_value == p.ab_value:
                            best_action = cur_node
                elif cur_node.depth == 0:
                    best_action = cur_node.sort_actions[0]
                continue
            if cur_node.alpha >= cur_node.bate:
                cur_node.child_index = len(actions)
                continue

            next_node: State = actions[cur_node.child_index].get_dst()
            next_node.alpha = cur_node.alpha
            next_node.bate = cur_node.bate
            next_node.depth = cur_node.depth + 1
            stacks.append(next_node)
            cur_node.child_index += 1
        state.set_best_action(best_action)

    def search_main(self, state: State, **kw):
        if self.search_type == AlphaBateSearch.AB_TYPE:
            return self.search_ab(state, [], depth=0, player_id=state.player_id, **kw)
        elif self.search_type == AlphaBateSearch.AB_MUCH:
            return self.search_ab_loop(state)
        return self.search_dfs(state, [], depth=0, player_id=state.player_id, **kw)


class AbDev(AlphaBateSearch):
    def get_depth_reward(self, s, **kw):
        self.state_num += 1
        return super().get_depth_reward(s, **kw)

    def search(self, state):
        self.state_num = 0
        return super().search(state)
