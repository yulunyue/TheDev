from .state import State, Action, MctsState
from .algo import Algo
from common.util.export import List, Dict, defaultdict, math, random, CT, logger
import time


class MctsSearch(Algo):

    def load(self, max_depath=-1, max_t=CT.inf, num_episodes=1000, **kw):
        self.exploration_param = 1.4
        self.max_depath = max_depath
        self.max_t = max_t / 1000
        self.num_episodes = num_episodes
        return super().load(**kw)

    def select(self, node: MctsState) -> MctsState:
        cur = node
        while not cur.game_over():
            cur = self.get_uct_best_child(cur)
        return cur

    def get_uct_best_child(self, cur: MctsState):
        best_score = -float("inf")
        best_child = None
        for a in cur.get_sort_actions():
            dst: MctsState = a.do().get_dst()
            dst.load_mcts(cur, a)
            score = dst.calc_uct_value(self.exploration_param)
            if score > best_score:
                best_score = score
                best_child = dst
        return best_child

    def simulate(self, root: State, max_round=1000):
        tail = root
        action_history: List[Action] = []
        while not tail.game_over():
            actions = tail.get_sort_actions()
            random_id = random.randint(0, len(actions) - 1)
            action_history.append(actions[random_id])
            max_round -= 1
            tail = actions[random_id].do().get_dst()
        return action_history

    def backpropagate(self, node: MctsState, score):
        node.mcts_update(score)

    def search_best_action(self, init_state: State, **kw):
        self.ep = 0
        self.start_time = time.time()
        while True:
            self.search_one_round(init_state)
            self.ep += 1
            cur_time = time.time()
            if self.ep >= self.num_episodes or cur_time - self.start_time >= self.max_t:
                break
        init_state.reset()
        return self.get_max_ct_action(init_state)

    def search_one_round(self, root):
        root.reset().load_mcts(None, None)
        node = self.select(root)  # 指导探索到待拓展的节点
        action = node.p_action
        if not node.game_over():
            node.expand()
            action = self.simulate(node.state)[-1]
        value = action.get_src_reward([action])
        self.backpropagate(node, value)

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
