from common.algo.search.state import State, Action
from common.algo.learn.base import Base
from common.util.export import List, Dict, defaultdict, math, random, CT


class MctsState(State):
    visite_num = 0
    visite_score = 0

    def __init__(self, state=None, player_id=0, depth=0):
        super().__init__(state, player_id, depth)
        self.expand_actions: List[Action] = []
        self.need_expand_actions: List[Action] = None

    def get_need_expand_actions(self):
        if self.need_expand_actions is not None:
            return self.need_expand_actions
        self.need_expand_actions = list(self.get_actions().values())
        return self.need_expand_actions

    def is_fully_expanded(self):
        return len(self.need_expand_actions) == 0

    def get_uct_best_child(self, exploration_param=1.4):
        best_score = -float("inf")
        best_child = None
        for action in self.expand_actions:
            child: MctsState = action.get_dst()
            # UCT公式
            exploit = child.visite_score / child.visite_num
            explore = exploration_param * math.sqrt(
                math.log(self.visite_num) / child.visite_num
            )
            score = exploit + explore
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def expand(self):
        self.expand_actions.append(self.get_need_expand_actions().pop())


class MctsSearch(Base):

    def load(self, max_depath=-1, num_episodes=50, **kw):
        self.c = math.sqrt(2.0)
        self.max_depath = max_depath
        return super().load(num_episodes=num_episodes, **kw)

    def select(self, node: MctsState, vt_states: List[MctsState]) -> MctsState:
        cur = node
        vt_states.append(cur)
        while not cur.is_game_over() and cur.is_fully_expanded():
            cur = cur.get_uct_best_child()
            vt_states.append(cur)
        return cur

    def take_action(self, node: MctsState) -> Action:
        max_score = -CT.inf
        ans = None
        for a in node.expand_actions:
            score = a.ucb_score()
            if score > max_score:
                ans = a
        return ans

    def backpropagate(self, vt_states: List[MctsState], score):
        for node in vt_states:
            node.visite_score += score
            node.visite_num += 1

    def search_main(self, init_state: MctsState):
        for _ in range(self.num_episodes):
            vt_states: List[MctsState] = []  # 不要用parent记录因为尽可能有多个parent，
            node = self.select(init_state, vt_states)  # 指导探索到为拓展的节点
            if not node.is_game_over():
                node = node.expand()
                vt_states.append(node)
            self.backpropagate(vt_states, node.get_reward())
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
