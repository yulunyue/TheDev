from common.algo.search.algo import Algo
from common.algo.search.state import State
import numpy as np
from typing import List


class EpsilonGreedy(Algo):
    def load(self, num_episodes=5000, epsilon=0.01, init_prob=1.0):
        self.init_prob = init_prob
        self.epsilon = epsilon
        return super().load(num_episodes=num_episodes)

    def run(self, state: State):
        self.regret_record = [0]
        self.actions = state.get_actions_all()
        self.estimates = [self.init_prob] * len(self.actions)
        self.counts = [0] * len(self.actions)

        for episode in range(self.num_episodes):
            action = self.get_action()
            reword, regret = state.get_reward(action), state.get_regret(action)
            self.regret_record.append(self.regret_record[-1] + regret)
            self.run_one_step(episode, action, reword)
        return self

    def get_action(self, *args):
        if np.random.rand() < self.epsilon:
            k = np.random.randint(0, len(self.actions))
        else:
            k = np.argmax(self.estimates)
        return k

    def run_one_step(self, episode, action, reward):
        self.counts[action] += 1
        self.estimates[action] += (
            1.0 / self.counts[action] * (reward - self.estimates[action])
        )

    def __str__(self):
        return ",".join(["%.3f" % v for v in self.estimates])


class DecayingEpsilonGreedy(EpsilonGreedy):
    total_count = 0

    def get_action(self, *args):
        self.total_count += 1
        if np.random.rand() < self.epsilon / self.total_count:
            k = np.random.randint(0, len(self.actions))
        else:
            k = np.argmax(self.estimates)
        return k


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
