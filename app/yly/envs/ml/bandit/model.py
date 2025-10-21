from common.algo.export import State, Action
from common.util.export import logger, List, Dict, ListUtil
import random
from typing import List


class Bandit(State):
    def __init__(self, k):
        super().__init__(k)
        self.k = k
        # self.probs = [random.random() for _ in range(k)]
        self.probs = [0.19, 0.77, 0.41, 0.46, 0.47, 0.43, 0.97, 0.17, 0.21, 0.62]
        self.max_idx, self.max_value = ListUtil(self.probs).max()

    def make_actions(self, **kw):
        actions = []
        for action in range(self.k):
            a = Action(self, action)
            actions.append(a)
        return actions

    def get_reward(self, a, **kw):
        return 1 if random.random() < self.probs[a] else 0

    def get_regret(self, a):
        return 0 if a == self.max_idx else -1
