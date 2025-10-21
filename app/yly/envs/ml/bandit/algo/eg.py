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
        return super().load()

    def take_action(self, state: Bandit):
        if random.rand() < self.epsilon / 1:
            return state.get_random_action()
        return self.get_max_action(state)

    def get_max_action(self, s: Bandit):
        actions = s.get_sort_actions()
        return ListUtil(actions).max(lambda a: self.action_value[a.action])

    def update_action(self, a: Action):
        r = a.get_reward()
        count, value = self.action_count[a.key], self.action_value[a.key]
        self.action_value[a.key] = (value * count + r) / (count + 1)
        self.action_count[a.key] += 1
