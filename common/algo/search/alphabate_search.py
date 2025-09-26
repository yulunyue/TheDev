from common.algo.search.state import State, inf, Action, AbState
from common.algo.search.algo import Algo
from typing import List, Dict
from common.util.export import logger, defaultdict, get_log, deque


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

        if depth == self.max_depth or state.get_done() is not None:
            return -self.get_depth_reward(state, depth)
        mvs: List[Action] = state.get_sort_actions(depth=depth)
        if not mvs:
            return -self.get_depth_reward(state, depth)
        state.best_action = None
        for a in mvs:
            reward = -self.search_ab(
                a.get_dst(),
                actions + [a],
                depth=depth + 1,
                alpha=-bate,
                bate=-alpha,
                player_id=player_id,
            )
            # self.debug("ab", actions + [a], f"r:{reward}")
            if reward >= bate:
                # self.debug(actions + [a], f"r:{reward},b:{bate}")
                alpha = bate
                self.set_state_best_action(state, a, actions)

                break
            elif reward > alpha:
                # self.debug(actions + [a], f"r:{reward},b:{alpha}")
                self.set_state_best_action(state, a, actions)
                alpha = reward
        return alpha

    def get_depth_reward(self, s: State, **kw):
        return s.get_self_reward(params=self.params)

    def search_dfs(
        self, state: State, actions: List[Action], depth=0, player_id=None, **kw
    ):
        if depth == self.max_depth or state.get_done() is not None:
            return -self.get_depth_reward(state, depth)
        mvs: List[Action] = state.get_sort_actions(depth=depth)
        if not mvs:
            return -self.get_depth_reward(state, depth)
        state.best_action = None
        best_reward = -inf
        for a in mvs:
            reward = -self.search_dfs(
                a.get_dst(), actions=actions + [a], depth=depth + 1, player_id=player_id
            )
            if reward > best_reward:
                state.set_best_action(a)
                best_reward = reward
        return best_reward

    def search_ab_loop(self, state: AbState):
        stacks = deque([state.load_ab()])

        pop_node: AbState = None
        stacks[0].search_depth = 0

        while stacks:
            cur_node = stacks[-1]
            if (
                cur_node.get_done() is not None
                or cur_node.search_depth == self.max_depth
            ):
                cur_node.ab_value = -self.get_depth_reward(cur_node)
                pop_node = stacks.pop()
                continue
            sort_actions = cur_node.get_sort_actions()
            if pop_node:
                reward = -pop_node.ab_value
                sa = sort_actions[cur_node.child_index - 1]
                if reward >= cur_node.bate:
                    cur_node.ab_value = cur_node.alpha = cur_node.bate
                    pop_node = stacks.pop()
                    continue
                if reward > cur_node.alpha:
                    # self.debug(stacks + [pop_node], f"r:{reward},a:{cur_node.alpha}")
                    cur_node.ab_value = cur_node.alpha = reward
                    cur_node.set_best_action(sa)
                # if cur_node.depth == 0:
                pop_node = None  # 根节点每次对比完 需要找新节点

            if cur_node.child_index >= len(sort_actions):
                pop_node = stacks.pop()
                continue
            cur_action = sort_actions[cur_node.child_index]
            next_node: AbState = cur_action.get_dst()
            next_node.load_ab(
                cur_node.search_depth + 1, -cur_node.bate, -cur_node.alpha
            )
            stacks.append(next_node)
            cur_node.child_index += 1

    def get_state_reward(self, s: AbState):
        return s.ab_value

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

    def search(self, state: State):
        self.state_num = 0
        ret = super().search(state)
        action = ret.action if ret else None
        self.logger.debug(state.show(title=f"BEGIN:{action}"))
        for a in sorted(
            state.get_sort_actions(),
            key=lambda a: self.get_state_reward(a.get_dst()),
        ):
            self.print_best_actions(a)
        return ret

    def set_state_best_action(self, s: State, a: Action, depth):
        super().set_state_best_action(s, a, depth)
