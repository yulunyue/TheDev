from common.algo.export import State, Action
from common.util.export import logger, List, Dict
import random
from typing import List


class BanditEnv:

    def load(self, k=10):
        self.pro = True
        self.K = k
        # self.probs = [random.random() for _ in range(self.K)]
        self.probs = [0.19, 0.77, 0.41, 0.46, 0.47, 0.43, 0.97, 0.17, 0.21, 0.62]
        self.max_idx = 0
        for j in range(1, self.K):
            if self.probs[j] > self.probs[self.max_idx]:
                self.max_idx = j
        return self

    def calc_reward(self, a):
        if a is None:
            return 0
        return 1 if random.random() < BAN_ENV.probs[a] else 0


BAN_ENV = BanditEnv()


class Bction(Action):

    def get_reward(self, **kw):
        return self.dst.get_reward()

    def get_regret(self):
        return BAN_ENV.probs[self.action] - BAN_ENV.probs[BAN_ENV.max_idx]

    def __repr__(self):
        return str(self.action)


class Bandit(State):

    def make_actions(self, **kw):
        actions = []
        for action in range(BAN_ENV.K):
            s = Bandit.new(action).set_done(1)
            a = Bction(self, action, s)
            actions.append(a)
        return actions

    def get_reward(self, actions=None, params=None):
        return BAN_ENV.calc_reward(self.state)
