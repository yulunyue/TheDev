from .state import State, Action
from .algo import Algo
from common.util.export import List, Dict, defaultdict, math, random, CT
import time


class MctsState:
    uct_score = 0

    def __init__(self, state: State):
        self.s = state
        self.expand_states: List[MctsState] = []
        self.need_expand_states: List[MctsState] = None
        self.visite_num = 0
        self.visite_score = 0

    def get_need_expand_states(self):
        if self.need_expand_states is not None:
            return self.need_expand_states
        self.need_expand_states = [
            MctsState(a.get_dst()) for a in self.s.get_sort_actions()
        ]
        return self.need_expand_states

    def is_fully_expanded(self):
        return len(self.get_need_expand_states()) == 0

    def get_uct_best_child(self, exploration_param=1.4):
        best_score = -float("inf")
        best_child = None
        for child in self.expand_states:

            score = self.calc_uct_value(child, exploration_param)
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def calc_uct_value(self, child: "MctsState", exploration_param):
        exploit = child.visite_score / child.visite_num
        explore = exploration_param * math.sqrt(
            math.log(self.visite_num) / child.visite_num
        )
        child.uct_score = exploit + explore
        return child.uct_score

    def expand(self):
        s = self.get_need_expand_states().pop()
        self.expand_states.append(s)
        return s

    def get_done(self):
        return self.s.get_done()

    def get_reward(self):
        return self.s.get_reward()


class MctsSearch(Algo):

    def load(self, max_depath=-1, max_t=-1, num_episodes=1000, **kw):
        self.c = math.sqrt(2.0)
        self.max_depath = max_depath
        self.max_t = max_t / 1000
        self.num_episodes = num_episodes
        return super().load(**kw)

    def select(self, node: MctsState) -> MctsState:
        cur = node
        self.vt_states.append(cur)
        while cur.get_done() is None and cur.is_fully_expanded():
            cur = cur.get_uct_best_child(self.c)
            self.vt_states.append(cur)
        return cur

    def simulate(self, node: MctsState):
        while node.get_done() is None:
            states = node.get_need_expand_states()
            random_id = random.randint(0, len(states) - 1)
            node = states[random_id]
        return node

    def backpropagate(self, score):
        for i in range(len(self.vt_states) - 1, -1, -1):
            self.back_vt(self.vt_states[i], score)

    def back_vt(self, s: MctsState, score):
        s.visite_score += score if s.s.player_id == 0 else -score
        s.visite_num += 1

    def search_main(self, init_state: State):
        self.ep = 0
        self.start_time = time.time()
        root = MctsState(init_state)
        while True:
            self.vt_states: List[MctsState] = []  # 不要用parent记录因为尽可能
            node = self.select(root)  # 指导探索到待拓展的节点
            if node.get_done() is None:
                expanded_node = node.expand()
                self.vt_states.append(expanded_node)
                end_node = self.simulate(expanded_node)
                self.backpropagate(end_node.get_reward())
            else:
                self.backpropagate(node.get_reward())
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
        for a in node.expand_states:
            if a.visite_num > best_visits:
                best_visits = a.visite_num
                best_state = a

        node.s.set_best_state(best_state.s)


class MctsSearchDev(MctsSearch):

    def back_vt(self, s, score):
        super().back_vt(s, score)
        s.s.set_headers(
            f"vt={s.visite_num}; vs={s.visite_score}; uct={'%.3f'%s.uct_score}; ep:{len(s.get_need_expand_states())}; vs:{len(s.expand_states)}"
        )

    def search(self, state):
        return super().search(state)
