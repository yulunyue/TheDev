from .eg import EpsilonGreedy
from ..model import Bandit
from common.third_util.np_util import np


class Ucb(EpsilonGreedy):

    def load(self, coef=1):
        self.coef = coef
        return super().load()

    def take_action(self, state: Bandit):
        actions = [v for v in state.get_actions().values()]
        estimates = np.array([self.action_value[v.key] for v in actions])
        counts = np.array([self.action_count[v.key] for v in actions])
        ucb = estimates + self.coef * np.sqrt(
            np.log(self.total_count) / (2 * counts + 1)
        )
        self.total_count += 1
        return actions[np.argmax(ucb)]
