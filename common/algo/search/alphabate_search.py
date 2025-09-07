from common.algo.search.state import State, inf, Action
from common.algo.search.algo import Algo
from typing import List, Dict
from common.util.export import logger, defaultdict, get_log


class AbState:
    def __init__(self, state: State, action=None, depth=0, alpha=-inf, bate=inf):
        self.state = state
        self.action = action
        self.child_index = 0
        self.alpha = alpha
        self.bate = bate
        self.depth = depth
        self.ab_value = alpha


class AlphaBateSearch(Algo):
    AB_TYPE = "alphabate"
    AB_MUCH = "abmuch"

    def debug(self, actions: List[Action], msg):
        if isinstance(actions[0], AbState):
            s = "".join([str(a.action.action) for a in actions[1:]])
        else:
            s = "".join([str(a.action) for a in actions])
        logger.debug(f"as:{s} {msg}")

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
            return -self.get_depth_reward(state)
        mvs: List[Action] = state.get_sort_actions(depth=depth)
        if not mvs:
            return -self.get_depth_reward(state)
        for a in mvs:
            reward = -self.search_ab(
                a.get_dst(),
                actions + [a],
                depth=depth + 1,
                alpha=-bate,
                bate=-alpha,
                player_id=player_id,
            )
            if reward >= bate:
                self.debug(actions + [a], f"r:{reward},b:{bate}")
                alpha = bate
                state.set_best_action(a)
                break
            if reward > alpha:
                self.debug(actions + [a], f"r:{reward},b:{alpha}")
                alpha = reward
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
            return -self.get_depth_reward(state)
        mvs: List[Action] = state.get_sort_actions(depth=depth)
        if not mvs:
            return -self.get_depth_reward(state)
        best_reward = -inf
        for a in mvs:
            reward = -self.search_dfs(
                a.get_dst(), actions=actions + [a], depth=depth + 1, player_id=player_id
            )
            if reward > best_reward:
                state.set_best_action(a)
                best_reward = reward
        return best_reward

    def search_ab_loop(self, state: State):
        stacks = [AbState(state)]

        pop_node: AbState = None
        state.depth = 0
        best_action = None
        while stacks:
            cur_node = stacks[-1]
            if cur_node.state.get_done() or cur_node.depth == self.max_depth:
                cur_node.ab_value = -self.get_depth_reward(cur_node.state)
                pop_node = stacks.pop()
                continue
            sort_actions = cur_node.state.get_sort_actions()
            if pop_node:
                # logger.debug(
                #     f"c: {cur_node.state.state},{cur_node.alpha} s: {pop_node.state.state},{pop_node.ab_value}"
                # )
                reward = -pop_node.ab_value
                if reward >= cur_node.bate:
                    # cur_node.child_index = len(actions)
                    self.debug(stacks + [pop_node], f"r:{reward},b:{cur_node.bate}")
                    cur_node.ab_value = cur_node.alpha = cur_node.bate
                    pop_node = stacks.pop()
                    # cur_node.ab_value = -pop_node.ab_value
                    continue
                if reward > cur_node.alpha:
                    self.debug(stacks + [pop_node], f"r:{reward},a:{cur_node.alpha}")
                    cur_node.ab_value = cur_node.alpha = reward
                    if cur_node.depth == 0:
                        best_action = sort_actions[cur_node.child_index - 1]
                if cur_node.depth == 0:
                    pop_node = None  # 根节点每次对比完 需要找新节点

            if cur_node.child_index >= len(sort_actions):
                pop_node = stacks.pop()
                continue
            cur_action = sort_actions[cur_node.child_index]
            next_node = AbState(
                cur_action.get_dst(),
                cur_action,
                cur_node.depth + 1,
                -cur_node.bate,
                -cur_node.alpha,
            )
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
