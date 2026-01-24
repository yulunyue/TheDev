from .eg import BaseAlgo
from ..model import Bandit, Action
from common.third_util.ml.np_util import np
from ..constant import C


class Ucb(BaseAlgo):

    def load(self, coef):
        self.coef = coef  # UCB 算法控制稳定性的因子
        self.estimates = np.array([1.0] * C.K)
        self.counts = np.zeros(C.K)
        self.total_count = 0
        return super().load()

    def take_action(self, state: Bandit):
        self.total_count += 1
        actions = state.get_sort_actions()
        ucb = self.estimates + self.coef * np.sqrt(
            np.log(self.total_count) / (2 * (self.counts + 1))
        )
        a = np.argmax(ucb)
        assert a == actions[a].action
        return actions[a]

    def update_action(self, a: Action, r):
        self.estimates[a.action] = (
            self.estimates[a.action] * self.counts[a.action] + r
        ) / (self.counts[a.action] + 1)
        self.counts[a.action] += 1
        return self

    def info(self):
        return [f"{self.estimates}", f"{self.counts}"]
