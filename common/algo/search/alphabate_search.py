from .states.state import State, inf, Action
from .states.abstate import AbState
from .algo import Algo
from common.util.export import (
    logger,
    defaultdict,
    get_log,
    deque,
    List,
    Dict,
)


class AlphaBateSearch(Algo):
    AB_TYPE = "alphabate"
    AB_MUCH = "abmuch"

    def load(self, max_depth, search_type="abmuch", **kw):
        self.max_depth = max_depth
        self.search_type = search_type
        return super().load(**kw)

    def search_dfs(
        self, state: AbState, actions: List[Action], depth=0, player_id=None, **kw
    ):
        if depth == self.max_depth or state.game_over():
            return -self.get_depth_reward(actions)
        mvs: List[Action] = state.get_sort_actions(depth=depth)
        if not mvs:
            return -self.get_depth_reward(actions)
        self.set_state_reward(state, -inf, inf)
        for a in mvs:
            a.do()
            reward = -self.search_dfs(
                a.get_dst(), actions=actions + [a], depth=depth + 1, player_id=player_id
            )
            a.undo()
            if reward > state.alpha:
                self.set_state_best_action(state, a, depth, reward)
        return state.alpha

    def search_ab(
        self, state: AbState, actions: List[Action], depth=0, alpha=-inf, bate=inf, **kw
    ) -> None:
        """
        -> 代表取反一次所以
        max_depth=1  s0->a0->-
        max_depth=2  s0->a1-s1->a1->-
        """
        if depth == self.max_depth or state.game_over():
            return -self.get_depth_reward(actions)
        mvs: List[Action] = state.get_sort_actions(depth=depth)
        if not mvs:
            return -self.get_depth_reward(actions)
        self.set_state_reward(state, alpha, bate)
        for a in mvs:
            a.do()
            reward = -self.search_ab(
                a.get_dst(),
                actions + [a],
                depth=depth + 1,
                alpha=-state.bate,
                bate=-state.alpha,
            )
            a.undo()
            if reward >= state.bate:
                state.alpha = state.bate
                break
            elif reward > state.alpha:
                self.set_state_best_action(state, a, actions, reward)
        return state.alpha

    def get_depth_reward(self, actions: List[Action], **kw):
        return actions[-1].get_src_reward(actions=actions)

    def set_state_reward(self, s: AbState, alpha, bate):
        s.alpha, s.bate = alpha, bate
        return self

    def set_state_best_action(
        self, state: AbState, a: Action, depth, reward, *args, **kw
    ):
        state.set_best_action(a)
        self.set_state_reward(state, reward, state.bate)

    def search_ab_loop(self, state: AbState):
        stacks = deque([state.load_ab()])
        pop_node: AbState = None
        while stacks:
            cur_node = stacks[-1]
            if cur_node.game_over() or cur_node.search_depth == self.max_depth:
                cur_node.alpha = -self.get_depth_reward([cur_action])
                pop_node = stacks.pop()
                continue
            sort_actions = cur_node.get_sort_actions()
            if pop_node:
                pop_node.p_action.undo()
                reward = -pop_node.alpha
                sa = sort_actions[cur_node.child_index - 1]
                if reward >= cur_node.bate:
                    cur_node.alpha = cur_node.bate
                    pop_node = stacks.pop()
                    continue
                if reward > cur_node.alpha:
                    self.set_state_best_action(
                        cur_node, sa, cur_node.search_depth, reward
                    )

                pop_node = None  # 根节点每次对比完 需要找新节点

            if cur_node.child_index >= len(sort_actions):
                pop_node = stacks.pop()
                continue
            cur_action = sort_actions[cur_node.child_index]
            next_node: AbState = cur_action.do().get_dst()
            next_node.load_ab(
                cur_node.search_depth + 1,
                -cur_node.bate,
                -cur_node.alpha,
                p_action=cur_action,
            )
            stacks.append(next_node)
            cur_node.child_index += 1

    def search_best_action(self, state: State, **kw):
        if self.search_type == AlphaBateSearch.AB_TYPE:
            self.search_ab(state, [], depth=0, player_id=state.player_id, **kw)
        elif self.search_type == AlphaBateSearch.AB_MUCH:
            self.search_ab_loop(state)
        else:
            self.search_dfs(state, [], depth=0, player_id=state.player_id, **kw)
        state.reset()
        return state.best_action


class AbDev(AlphaBateSearch):
    def get_depth_reward(self, actions: List[Action], *args, **kw):
        # log.info(actions[-1].show())
        # log.info(actions[-1].get_dst().show())
        self.state_num += 1
        return super().get_depth_reward(actions, *args, **kw)

    def search(self, state: State, **kw):
        self.state_num = 0
        ret = super().search(state)
        return ret

    def set_state_reward(self, s: State, alpha, bate):

        ret = super().set_state_reward(s, alpha, bate)
        # self.logger.debug(s.show())
        return ret

    def set_state_best_action(self, s: State, a: Action, depth, reward):
        # log1.info(f"{a.show()} reward:{reward} \n{s.show()}")
        super().set_state_best_action(s, a, depth, reward)
        # self.logger.debug(s.show_best_actions())

    def info(self):
        return [f"state_num:{self.state_num}"]
