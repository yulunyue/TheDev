from .states.action import Action
from .states.mctsstate import MctsState
from .algo import Algo
from common.util.export import (
    List,
    Dict,
    defaultdict,
    math,
    random,
    CT,
    logger,
    time,
    Tuple,
)


class MctsSearch(Algo):

    def load(
        self,
        max_depath=-1,
        max_t=CT.inf,
        num_episodes=1000,
        exploration_param=1.4,
        **kw,
    ):
        self.exploration_param = exploration_param
        self.max_depath = max_depath
        self.max_t = max_t / 1000
        self.num_episodes = num_episodes
        return super().load(**kw)

    def select(self, node: MctsState) -> Tuple[MctsState, List[Action]]:
        cur = node
        ret = []
        while cur.has_visited and not cur.game_over():
            a = self.get_uct_best_child(cur)
            ret.append(a)
            cur = a.dst
        if not cur.has_visited:
            cur.load_mcts(None if not ret else ret[-1])

        return cur, ret

    def get_uct_best_child(self, cur: MctsState):
        return self.get_best_action(
            cur, lambda a: a.calc_uct_value(self.exploration_param)
        )

    def simulate(self, root: MctsState, max_round=1000):
        tail = root
        action_history: List[Action] = []
        while not tail.game_over() and max_round:
            a = tail.get_random_action()
            action_history.append(a)
            max_round -= 1
            tail = a.do().dst
        return action_history

    def backpropagate(
        self, actions: List[Action], simu_actions: List[Action], leaf_value
    ):
        for i in range(len(actions) - 1, -1, -1):
            s = actions[i].src
            c = -1 if s.mode == s.MAN2 else 1
            s.n_visits += 1
            s.q += 1.0 * (leaf_value - s.q) / s.n_visits
            leaf_value *= c

    def search_best_action(self, init_state: MctsState, **kw):
        self.ep = 0
        self.start_time = time.time()
        init_state.load_mcts(None)
        while True:
            self.search_one_round(init_state)
            self.ep += 1
            cur_time = time.time()
            if self.ep >= self.num_episodes or cur_time - self.start_time >= self.max_t:
                break
        init_state.reset()
        return self.get_max_ct_action(init_state)

    def search_one_round(self, root: MctsState):
        root.reset()
        node, actions = self.select(root)  # 指导探索到待拓展的节点
        last_action = actions[-1]
        simu_actions = []
        if not node.game_over():
            node.expand()
            simu_actions = self.simulate(node)
            last_action = simu_actions[-1]
        value = last_action.get_src_reward(simu_actions + actions)
        self.backpropagate(actions, simu_actions, value)

    def get_max_ct_action(self, node: MctsState):
        """
        UCT公式用于搜索过程中的节点选择，目的是平衡探索与利用
        访问次数用于最终决策中的移动选择，目的是选择最可靠、最经过验证的移动
        所以这使用访问次数
        """
        best_action = None
        best_visits = -1
        for a in node.get_sort_actions():
            d = a.get_dst()
            if d.n_visits > best_visits:
                best_visits = d.n_visits
                best_action = a
        return best_action


class MctsSearchDev(MctsSearch):

    def search(self, state, **kw):
        action: Action = super().search(state, **kw)
        return action

    def info(self):
        ret = [f"ep:{self.ep}"]

        def util(c: MctsState, depth=1):
            if not c.n_visits:
                return
            ret.append(c.show())
            if not c.children or depth == 0:
                return
            for d in c.children:
                util(d, depth - 1)

        util(self.root)
        return ret
