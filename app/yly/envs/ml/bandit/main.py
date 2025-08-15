from common.algo.export import State, Action
from common.util.export import logger, List, Dict
import random
from typing import List


class BanditEnv:

    def load(self, k=10):
        self.pro = True
        self.K = k
        self.probs = [random.random() for _ in range(self.K)]
        self.max_idx = 0
        for j in range(1, self.K):
            if self.probs[j] > self.probs[self.max_idx]:
                self.max_idx = j
        return self

    def calc_reward(self, a):
        return 1 if random.random() < BAN_ENV.probs[a] else 0


BAN_ENV = BanditEnv()


class Bction(Action):

    def get_reward(self, **kw):
        return BAN_ENV.calc_reward(self.action)

    def get_regret(self):
        return BAN_ENV.probs[self.action] - BAN_ENV.probs[BAN_ENV.max_idx]

    def __repr__(self):
        return str(self.action)


class Bandit(State):

    def make_actions(self, **kw) -> Dict[int, Bction]:
        actions = dict()
        for action in range(BAN_ENV.K):
            a = Bction(self, action, Bandit.new(action).set_done(True))
            actions[action] = a
        return actions
