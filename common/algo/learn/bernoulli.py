from common.algo.search.algo import Algo
from common.algo.search.state import State, Action
import numpy as np
from typing import List


class EpsilonGreedy(Algo):
    def load(self, use_cache=False, max_t=-1, num_episodes=5000, epsilon=0.1):
        return super().load(use_cache, max_t, num_episodes, epsilon)

    def take_action(self, state: State):
        if np.random.rand() < self.epsilon:
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
        reward = a.get_reward()
        a.value += reward
        self.reward_change(reward)


class DecayingEpsilonGreedy(EpsilonGreedy):
    total_count = 0

    def take_action(self, state: State):
        self.total_count += 1
        if np.random.rand() < self.epsilon / self.total_count:
            actions = list(state.get_actions().values())
            k = np.random.randint(0, len(actions))
            return actions[k]
        return self.get_max_action(state)


class Ucb(EpsilonGreedy):
    total_count = 0

    def load(self, num_episodes=5000, coef=1):
        self.coef = coef
        return super().load(num_episodes=num_episodes)

    def get_action(self, *args):
        self.total_count += 1
        ucb = np.array(self.estimates) + self.coef * np.sqrt(
            np.log(self.total_count) / (2 * (np.array(self.counts) + 1))
        )
        return np.argmax(ucb)


class ThompsonSampling(EpsilonGreedy):

    def get_action(self, *args):
        samples = np.random.beta(self.a, self.b)
        return np.argmax(samples)

    def run_one_step(self, episode, action, reward):
        self.a[action] += reward
        self.b[action] += 1 - reward

    def run(self, state: State):
        self.a = np.ones(len(state.get_actions_all()))
        self.b = np.ones(len(state.get_actions_all()))
        return super().run(state)
