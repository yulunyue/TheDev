from common.algo.search.state import State, Action
from common.algo.learn.base import Base
from common.util.export import List, Dict, defaultdict, math, random, CT


class MctsSearch(Base):

    def load(self, max_depath=-1, num_episodes=50, **kw):
        self.c = math.sqrt(2.0)
        self.max_depath = max_depath
        return super().load(num_episodes=num_episodes, **kw)

    def select(self, node: State) -> tuple[State, int]:
        score = 0
        max_depath = self.max_depath
        while node.expand_actions and max_depath != 0:
            if node.get_done():
                return node, score
            a = self.take_action(node)
            node = a.get_dst()
            node.parent = a.src
            score += a.get_reward()
            max_depath -= 1
        if not node.expand_actions:
            node.expand_actions = node.get_sort_actions(params=self.params)
        return node, score

    def take_action(self, node: State) -> Action:
        max_score = -CT.inf
        ans = None
        for a in node.expand_actions:
            score = a.ucb_score()
            if score > max_score:
                ans = a
        return ans

    def backpropagate(self, node: State, score):
        while node:
            node.visite_score += score
            node.visite_num += 1
            node = node.parent

    def search_main(self, init_state: State):
        if init_state.get_done():
            return
        for _ in range(self.num_episodes):
            dst, score = self.select(init_state)
            self.backpropagate(dst, score)
        init_state.set_best_action(self.take_action(init_state))
