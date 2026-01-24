from .state import State, Action
from .algo import Algo
from common.util.export import List, Dict, defaultdict, math, random, CT, logger
import time


class MctsState:

    def __init__(self, state: State, p: "MctsState" = None, p_action=None):
        self.state = state
        self.children = None
        self.n_visits = 0
        self.u = 0
        self.q = 0
        self.p: MctsState = p
        # state.extra = self
        self.leaf_value = 0
        self.p_action: Action = p_action

    def get_children(self):
        if self.children is not None:
            return self.children
        self.children = []
        for a in self.state.get_sort_actions():
            self.children.append(MctsState(a.do().get_dst(), self, a))
            a.undo()
        return self.children

    def update(self, leaf_value):
        if self.p:
            self.p.update(-leaf_value)
        self.n_visits += 1
        self.q += 1.0 * (leaf_value - self.q) / self.n_visits

    def calc_uct_value(self, exploration_param):
        self.u = exploration_param * math.sqrt(self.p.n_visits / (self.n_visits + 1))
        return self.q + self.u

    def expand(self):
        return self.get_children()

    def is_leaf(self):
        return self.state.game_over() or self.children is None

    def show(self):
        msg = f"s={self.state.state}; depth:{self.state.depth}; vt={self.n_visits}; q={'%.3f'%self.q}; u={'%.3f'%self.u};"
        return self.state.show(msg)


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
            score = child.calc_uct_value(self.exploration_param)
            if score > best_score:
                best_score = score
                best_child = child
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
        node.update(score)

    def search_best_action(self, init_state: State, **kw):
        self.ep = 0
        self.start_time = time.time()
        self.root = MctsState(init_state)
        while True:
            self.root.state.reset()
            node = self.select(self.root)  # 指导探索到待拓展的节点
            action = node.p_action
            if not node.state.game_over():
                node.expand()
                action = self.simulate(node.state)[-1]
            value = action.get_src_reward([action])
            self.backpropagate(node, value)
            self.ep += 1
            cur_time = time.time()
            if self.ep >= self.num_episodes or cur_time - self.start_time >= self.max_t:
                break
        self.root.state.reset()
        return self.get_max_ct_action(self.root)

    def get_max_ct_action(self, node: MctsState):
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
        return best_state.p_action


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
