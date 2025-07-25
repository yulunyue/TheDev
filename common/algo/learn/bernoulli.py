from common.algo.learn import Algo
from common.algo.search.state import State, Action
import numpy as np
from typing import List


class EpsilonGreedy(Algo):

    def load(self, use_cache=False, max_t=-1, num_episodes=5000, epsilon=0.01):
        self.total_count = 1
        return super().load(use_cache, max_t, num_episodes, epsilon)

    def take_action(self, state: State):
        if np.random.rand() < self.epsilon / self.total_count:
            actions = list(state.get_actions().values())
            k = np.random.randint(0, len(actions))
            return actions[k]
        return self.get_max_action(state)

    def get_max_action(self, s: State):
        actions = list(s.get_actions().values())
        k = np.argmax([v.value for v in actions])
        return actions[k]

    def run_one(self, state: State):
        a = self.take_action(state)
        regrat, r = a.get_reward()
        a.value = (a.value * a.count + r) / (a.count + 1)
        a.count += 1
        self.reward_tmp_all -= regrat

    def search(self, state: State):
        for a in state.get_actions().values():
            a.value = 1
            a.count = 0
        return super().search(state)


class DecayingEpsilonGreedy(EpsilonGreedy):

    def take_action(self, state: State):
        r = super().take_action(state)
        self.total_count += 1
        return r


class Ucb(EpsilonGreedy):

    def load(self, num_episodes=5000, coef=1):
        self.coef = coef
        return super().load(num_episodes=num_episodes)

    def run_one(self, state: State):
        a = self.get_max_action(state)
        regrat, r = a.get_reward()
        a.value = (a.value * a.count + r) / (a.count + 1)
        a.count += 1
        self.reward_tmp_all -= regrat

    def get_max_action(self, state):
        actions = [v for v in state.get_actions().values()]
        estimates = [v.value for v in actions]
        counts = [v.count for v in state.get_actions().values()]
        ucb = np.array(estimates) + self.coef * np.sqrt(
            np.log(self.total_count) / (2 * (np.array(counts) + 1))
        )
        self.total_count += 1
        return actions[np.argmax(ucb)]


class ThompsonSampling(Algo):

    def load(self, use_cache=False, max_t=-1, num_episodes=5000, epsilon=0.01):
        return super().load(use_cache, max_t, num_episodes, epsilon)

    def run_one(self, state: State):
        a = self.get_max_action(state)
        regrat, reward = a.get_reward()
        self.reward_tmp_all -= regrat
        a.value[0] += reward
        a.value[1] += 1 - reward

    def search(self, state: State):
        for a in state.get_actions().values():
            a.value = [1, 1]
        return super().search(state)

    def get_max_action(self, state):
        actions = [state.get_action(i) for i in range(state.action_size())]
        a = [ac.value[0] for ac in actions]
        b = [ac.value[1] for ac in actions]
        samples = np.random.beta(a, b)
        k = np.argmax(samples)
        return actions[k]
