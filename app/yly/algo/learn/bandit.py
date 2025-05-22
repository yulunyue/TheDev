from common.algo.export import State, np, Action
import random
from typing import List


class Bandit(State):
    K = 10

    def __init__(self):
        self.probs = [random.random() for _ in range(self.K)]
        self.max_idx = 0
        for j in range(1, self.K):
            if self.probs[j] > self.probs[self.max_idx]:
                self.max_idx = j

    def get_reward(self, action):
        return 1 if random.random() < self.probs[action] else 0

    def get_regret(self, action):
        return self.probs[self.max_idx] - self.probs[action]

    def __str__(self):
        return ",".join(["%.3f" % float(v) for v in self.probs])

    def get_actions_all(self):
        return list(range(self.K))
