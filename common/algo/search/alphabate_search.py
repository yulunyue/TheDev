from common.algo.search.state import State, inf, Action
from common.algo.search.algo import Algo
from typing import List, Dict
from common.util.export import logger, defaultdict, get_log, deque


class AbState:
    def __init__(self, state: State, action=None, depth=0, alpha=-inf, bate=inf):
        self.state: State = state
        self.action: Action = action
        self.child_index = 0
        self.alpha = alpha
        self.bate = bate
        self.depth = depth
        self.ab_value = alpha

    def __repr__(self):
        a = self.action.action if self.action else "?"
        return f"idx:{self.child_index}, a:{a}, d:{self.depth}"

    def set_best_action(self, a: Action, eq_flag, reward):
        if not eq_flag or self.state.best_action is None:
            self.state.set_best_action(a)
            return


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
            return -self.get_depth_reward(state), depth
        mvs: List[Action] = state.get_sort_actions(depth=depth)
        if not mvs:
            return -self.get_depth_reward(state), depth
        best_action: Action = None
        for a in mvs:
            reward, a.depth = self.search_ab(
                a.get_dst(),
                actions + [a],
                depth=depth + 1,
                alpha=-bate,
                bate=-alpha,
                player_id=player_id,
            )
            reward = -reward
            # self.debug("ab", actions + [a], f"r:{reward}")
            if reward >= bate:
                # self.debug(actions + [a], f"r:{reward},b:{bate}")
                alpha = bate
                best_action = a
                break
            elif reward == bate:
                alpha = bate
                if reward <= 0:
                    if best_action.depth < a.depth:
                        best_action = a
                else:
                    if best_action.depth > a.depth:
                        best_action = a
                break
            elif reward > alpha or best_action is None:
                # self.debug(actions + [a], f"r:{reward},b:{alpha}")
                best_action = a
                alpha = reward
            elif reward == alpha:
                alpha = reward
                if reward <= 0:
                    if best_action.depth < a.depth:
                        best_action = a
                else:
                    if best_action.depth > a.depth:
                        best_action = a

        state.set_best_action(best_action)
        return alpha, best_action.depth

    def get_depth_reward(
        self, s: State, depth: int = None, actions: List[Action] = None, **kw
    ):
        return s.get_self_reward(depth=depth, actions=actions, params=self.params)

    def search_dfs(
        self, state: State, actions: List[Action], depth=0, player_id=None, **kw
    ):
        if depth == self.max_depth or state.get_done() is not None:
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
        stacks = deque([AbState(state)])

        pop_node: AbState = None
        stacks[0].depth = 0

        while stacks:
            cur_node = stacks[-1]
            if (
                cur_node.state.get_done() is not None
                or cur_node.depth == self.max_depth
            ):
                cur_node.ab_value = -self.get_depth_reward(cur_node.state)
                pop_node = stacks.pop()
                max_depth = cur_node.depth
                continue
            sort_actions = cur_node.state.get_sort_actions()
            if pop_node:
                reward = -pop_node.ab_value
                # self.debug(
                #     "sk", stacks + [pop_node], f"r:{reward}, s:{pop_node.state.state}"
                # )
                sa = sort_actions[cur_node.child_index - 1]
                if reward >= cur_node.bate:
                    # cur_node.child_index = len(actions)
                    # self.debug(stacks + [pop_node], f"r:{reward},b:{cur_node.bate}")
                    cur_node.ab_value = cur_node.alpha = cur_node.bate
                    # cur_node.state.set_best_action(
                    #     sort_actions[cur_node.child_index - 1]
                    # )
                    pop_node = stacks.pop()
                    cur_node.set_best_action(sa, reward == cur_node.bate, reward)
                    # cur_node.ab_value = -pop_node.ab_value
                    continue
                if reward >= cur_node.alpha:
                    # self.debug(stacks + [pop_node], f"r:{reward},a:{cur_node.alpha}")
                    cur_node.set_best_action(sa, reward == cur_node.alpha, reward)
                    cur_node.ab_value = cur_node.alpha = reward

                # if cur_node.depth == 0:
                pop_node = None  # 根节点每次对比完 需要找新节点

            if cur_node.child_index >= len(sort_actions):
                pop_node = stacks.pop()
                continue
            cur_action = sort_actions[cur_node.child_index]
            cur_action.depth = cur_node.depth + 1
            next_node = AbState(
                cur_action.get_dst(),
                cur_action,
                cur_node.depth + 1,
                -cur_node.bate,
                -cur_node.alpha,
            )
            stacks.append(next_node)
            cur_node.child_index += 1

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
        self.print_best_actions(state)
        return ret

    # def debug(self, name, actions: List[Action], msg=""):
    #     if actions and isinstance(actions[0], AbState):
    #         s = "".join([str(a.action.action) for a in actions[1:]])
    #     else:
    #         s = "".join([str(a.action) for a in actions])
    #     get_log(name).debug(f"as:{s} {msg}")
