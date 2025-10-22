from common.algo.export import Algo
from common.third_util.np_util import np
from common.util.export import defaultdict, random, ListUtil
from ..model import Bandit, Action
from .base import BaseAlgo


class EpsilonGreedy(BaseAlgo):

    def load(self, epsilon):
        self.action_count = defaultdict(int)
        self.action_value = defaultdict(lambda: 0)
        self.epsilon = epsilon
        self.total_count = 1
        return super().load()

    def take_action(self, state: Bandit):
        if random.random() < self.epsilon / self.total_count:
            return state.get_random_action()
        return self.get_max_action(state)

    def get_max_action(self, s: Bandit):
        actions = s.get_sort_actions()
        return ListUtil(actions).max(lambda a: self.action_value[a.action])[1]

    def update_action(self, a: Action, r):
        n, v = self.action_count[a.action], self.action_value[a.action]
        self.action_value[a.action] = (v * n + r) / (n + 1)
        self.action_count[a.action] = n + 1

    def info(self):
        return [f"v:{dict(self.action_value)}", f"c:{dict(self.action_count)}"]
