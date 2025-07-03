from common.algo.export import State, Action
from common.util.export import logger
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

    def use_pro(self, pro):
        self.pro = pro
        return self

    def calc_reward(self, a):
        if not self.pro:
            return BAN_ENV.probs[a]
        return 1 if random.random() < BAN_ENV.probs[a] else 0


BAN_ENV = BanditEnv()


class Bction(Action):
    def get_reward(self, **kw):
        return BAN_ENV.calc_reward(self.action)


class Bandit(State):
    reward = 0

    def __init__(self, state="", player_id=0, depth=1):
        super().__init__(state, player_id, depth)

    def gen_action(self, a):
        return Bction(self, a, Bandit(self.state + str(a))).set_value(0)

    def get_actions_all(self):
        return list(range(BAN_ENV.K))

    def __repr__(self):
        return str([v.value for v in self.get_actions().values()])
