from common.algo.search.state import State, Action
from common.algo.learn.base import Base
from typing import List, Dict
import math
import random
import numpy as np
import time

inf = float("inf")



class MctsSearch(Base):

    def load(self, **kw):
        self.scalar = 1 / (2 * math.sqrt(2.0))  # 0.353553
        return super().load(**kw)

    def select(self, node: State, visite_actions: List[Action]):
        score = 0
        while node.expand_actions:
            action = max(node.expand_actions, key=lambda v: self.ucb_score(v))
            visite_actions.append(node)
            score += action.reward
            node = action.dst
        return node, score

    def expand(self, node: State, visite_actions: List[Action]):
        untried_actions = node.get_untried_actions()
        i = random.randint(0, len(untried_actions) - 1)
        child = untried_actions.pop(i)
        node.expand_actions.append(child)
        visite_actions.append(child)
        return child.dst, child.reward

    def backpropagate(self, actions: List[Action], score):
        for a in actions:
            a.dst.visite_num += 1
            a.dst.mct_value += score
            self.reward_tmp_all += a.reward

    def simulate(self, cur: State):
        value = 0
        visite_actions: List[Action] = []
        while not cur.done:
            if not cur.is_visite:
                cur.is_visite = True
                cur, score = self.expand(cur, visite_actions)
            elif self.can_epsilon() and cur.get_untried_actions():
                cur, score = self.expand(cur, visite_actions)
            else:
                cur, score = self.select(cur, visite_actions)
            value += score
        return visite_actions, value

    def ucb_score(self, a: Action):
        exploit = a.dst.mct_value / a.dst.visite_num  # 平均值
        explore = math.sqrt(2.0 * math.log(a.src.visite_num) / a.src.visite_num)
        a.value = exploit + self.scalar * explore
        return a.value

    def search_main(self, init_state: State):
        for _ in range(self.num_episodes):
            visite_actions, score = self.simulate(init_state)
            self.backpropagate(visite_actions, score)
        init_state.set_best_action(self.get_max_action(init_state))

    def get_max_action(self, state: State):
        actions = list(state.get_actions().values())
        actions.sort(key=lambda a: a.dst.visite_num)
        return actions[-1]
