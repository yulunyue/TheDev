from common.algo.search.state import State, Action, MctsState
from common.algo.learn.base import Base
from common.util.export import List, Dict, defaultdict, math, random, CT
import time


class MctsSearch(Base):

    def load(self, max_depath=-1, num_episodes=5000, max_t=-1, **kw):
        self.c = math.sqrt(2.0)
        self.max_depath = max_depath
        self.max_t = max_t / 1000
        return super().load(num_episodes=num_episodes, **kw)

    def select(self, node: MctsState, vt_states: List[MctsState]) -> MctsState:
        cur = node
        vt_states.append(cur)
        while cur.get_done() is None and cur.is_fully_expanded():
            cur = cur.get_uct_best_child(self.c)
            vt_states.append(cur)
        return cur

    def simulate(self, node: MctsState):
        while node.get_done() is None:
            a = node.get_random_action()
            node = a.get_dst()
        return node

    def backpropagate(self, vt_states: List[MctsState], end_node: MctsState):
        n = len(vt_states)

        for i in range(n - 1, -1, -1):
            vt_states[i].visite_score += (
                1 if vt_states[i].player_id == end_node.player_id else -1
            )
            vt_states[i].visite_num += 1

    def search_main(self, init_state: MctsState):
        self.ep = 0
        self.start_time = time.time()
        while True:
            vt_states: List[MctsState] = []  # 不要用parent记录因为尽可能有多个parent，
            node = self.select(init_state, vt_states)  # 指导探索到待拓展的节点
            if node.get_done() is None:
                expanded_node = node.expand()
                vt_states.append(expanded_node)
                end_node = self.simulate(expanded_node)
                self.backpropagate(vt_states, end_node)
            else:
                self.backpropagate(vt_states, node)
            self.ep += 1
            cur_time = time.time()
            if self.ep >= self.num_episodes or cur_time - self.start_time >= self.max_t:
                break
        init_state.set_best_action(self.get_max_action(init_state))

    def get_max_action(self, node: MctsState):
        """
        UCT公式用于搜索过程中的节点选择，目的是平衡探索与利用
        访问次数用于最终决策中的移动选择，目的是选择最可靠、最经过验证的移动
        所以这使用访问次数
        """
        best_move = None
        best_visits = -1
        for a in node.get_actions().values():
            if a.get_dst().visite_num > best_visits:
                best_visits = a.get_dst().visite_num
                best_move = a
        return best_move


class MctsSearchDev(MctsSearch):
    def backpropagate(self, vt_states: List[MctsState], node: MctsState):
        ret = super().backpropagate(vt_states, node)
        self.log(f"[MctsSearchDev {self.ep}]")
        for i in range(1, min(len(vt_states), 3)):
            self.log(vt_states[i].show())
        self.log(node.show())
        return ret

    def search(self, state):
        self.log(state.show())
        return super().search(state)
