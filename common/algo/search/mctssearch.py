from .state import State, Action
from .algo import Algo
from common.util.export import List, Dict, defaultdict, math, random, CT
import time


class MctsState:

    def __init__(self, state: State, p: "MctsState" = None, p_action=None):
        self.state = state
        self.children = None
        self.n_visits = 0
        self.u = 0
        self.q = 0
        self.p: MctsState = p
        self.p_action = p_action

    def get_children(self):
        if self.children is not None:
            return self.children
        self.children = [
            MctsState(d.get_dst(), self, d) for d in self.state.get_sort_actions()
        ]
        return self.children

    def update(self, leaf_value):
        if self.p:
            self.p.update(-leaf_value)
        self.n_visits += 1
        self.q += 1.0 * (leaf_value - self.q) / self.n_visits

    def expand(self):
        return self.get_children()

    def is_leaf(self):
        return self.state.game_over or self.children is None

    def __str__(self):
        return f"vt={self.n_visits}; q={'%.3f'%self.q}; u={'%.3f'%self.u}"


class MctsSearch(Algo):

    def load(self, max_depath=-1, max_t=CT.inf, num_episodes=1000, **kw):
        self.exploration_param = 1.4
        self.max_depath = max_depath
        self.max_t = max_t / 1000
        self.num_episodes = num_episodes
        return super().load(**kw)

    def select(self, node: MctsState) -> MctsState:
        cur = node
        while not cur.is_leaf():
            cur = self.get_uct_best_child(cur)
        return cur

    def get_uct_best_child(self, cur: MctsState):
        best_score = -float("inf")
        best_child = None
        for child in cur.get_children():
            score = self.calc_uct_value(child)
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def calc_uct_value(self, c: "MctsState"):
        c.u = self.exploration_param * math.sqrt(c.p.n_visits / (c.n_visits + 1))
        return c.q + c.u

    def simulate(self, root: State):
        tail = root
        while not tail.game_over:
            actions = tail.get_sort_actions()
            random_id = random.randint(0, len(actions) - 1)
            tail = actions[random_id].get_dst()
        reward = tail.get_self_reward()
        return reward if root.player_id == tail.player_id else -reward

    def backpropagate(self, node: MctsState, score):
        while node:
            self.update(node, score)
            node = node.p
            score = -score

    def update(self, node: MctsState, score):
        node.update(score)

    def search_main(self, init_state: State):
        self.ep = 0
        self.start_time = time.time()
        root = MctsState(init_state)
        while True:
            node = self.select(root)  # 指导探索到待拓展的节点
            if not node.state.game_over:
                node.expand()
            value = self.simulate(node.state)
            self.backpropagate(node, value)
            self.ep += 1
            cur_time = time.time()
            if self.ep >= self.num_episodes or cur_time - self.start_time >= self.max_t:
                break
        self.update_max_action(root)

    def update_max_action(self, node: MctsState):
        """
        UCT公式用于搜索过程中的节点选择，目的是平衡探索与利用
        访问次数用于最终决策中的移动选择，目的是选择最可靠、最经过验证的移动
        所以这使用访问次数
        """
        best_state = None
        best_visits = -1
        for a in node.get_children():
            if a.n_visits > best_visits:
                best_visits = a.n_visits
                best_state = a
        node.state.set_best_action(best_state.p_action)


class MctsSearchDev(MctsSearch):

    def update(self, s: MctsState, score):
        super().update(s, score)
        s.state.set_headers(str(s))

    def search(self, state):
        return super().search(state)
