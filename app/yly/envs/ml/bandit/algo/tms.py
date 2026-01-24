from .eg import EpsilonGreedy, Action, Bandit
from common.util.export import defaultdict
from common.third_util.ml.np_util import np


class ThompsonSampling(EpsilonGreedy):

    def load(self, num_episodes=5000, epsilon=0.01):
        self.action_value = defaultdict(lambda: [1, 1])
        return super().load(num_episodes=num_episodes, epsilon=epsilon)

    def update_action(self, a: Action):
        r = a.get_reward()
        self.action_value[a.key][0] += r
        self.action_value[a.key][1] += 1 - r

    def take_action(self, state: Bandit):
        actions = list(state.get_actions().values())
        a = [self.action_value[ac.key][0] for ac in actions]
        b = [self.action_value[ac.key][1] for ac in actions]
        samples = np.random.beta(a, b)
        k = np.argmax(samples)
        return actions[k]
