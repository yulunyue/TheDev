from common.algo.learn.base import Base
from common.algo.search.state import State, Action
import numpy as np
from typing import List
from common.util.export import defaultdict


class EpsilonGreedy(Base):

    def load(self, epsilon=0.1):
        self.action_count = defaultdict(int)
        self.action_value = defaultdict(lambda: 1)
        self.total_count = 1
        return super().load(epsilon=epsilon)

    def take_action(self, state: State):
        if np.random.rand() < self.epsilon / self.total_count:
            actions = list(state.get_actions().values())
            k = np.random.randint(0, len(actions))
            return actions[k]
        return self.get_max_action(state)

    def get_max_action(self, s: State):
        actions = list(s.get_actions().values())
        k = np.argmax([self.action_value[v.key] for v in actions])
        return actions[k]

    def update_action(self, a: Action):
        r = a.get_reward()
        count, value = self.action_count[a.key], self.action_value[a.key]
        self.action_value[a.key] = (value * count + r) / (count + 1)
        self.action_count[a.key] += 1


class DecayingEpsilonGreedy(EpsilonGreedy):

    def take_action(self, state: State):
        r = super().take_action(state)
        self.total_count += 1
        return r


class Ucb(EpsilonGreedy):

    def load(self, coef=1):
        self.coef = coef
        return super().load()

    def take_action(self, state: State):
        actions = [v for v in state.get_actions().values()]
        estimates = np.array([self.action_value[v.key] for v in actions])
        counts = np.array([self.action_count[v.key] for v in actions])
        ucb = estimates + self.coef * np.sqrt(
            np.log(self.total_count) / (2 * counts + 1)
        )
        self.total_count += 1
        return actions[np.argmax(ucb)]


class ThompsonSampling(Base):

    def load(self, num_episodes=5000, epsilon=0.01):
        self.action_value = defaultdict(lambda: [1, 1])
        return super().load(num_episodes=num_episodes, epsilon=epsilon)

    def update_action(self, a: Action):
        r = a.get_reward()
        self.action_value[a.key][0] += r
        self.action_value[a.key][1] += 1 - r

    def take_action(self, state: State):
        actions = list(state.get_actions().values())
        a = [self.action_value[ac.key][0] for ac in actions]
        b = [self.action_value[ac.key][1] for ac in actions]
        samples = np.random.beta(a, b)
        k = np.argmax(samples)
        return actions[k]
