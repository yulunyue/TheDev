from common.algo.export import State, Action
from common.util.export import logger
import random
from typing import List


class BanditEnv:

    def load(self, k=10):
        self.K = k
        self.probs = [random.random() for _ in range(self.K)]
        self.max_idx = 0
        for j in range(1, self.K):
            if self.probs[j] > self.probs[self.max_idx]:
                self.max_idx = j

    def calc_reward(self, a):
        # return 1 if random.random() < BAN_ENV.probs[a] else 0
        return self.probs[a]


BAN_ENV = BanditEnv()


class BanAction(Action):

    def __repr__(self):
        return f"s: {self.dst.state}; action: {self.action}; r: {self.dst.reward}"


class Bandit(State):
    reward = 0

    def gen_action(self, a):
        ret = BanAction(self, a, Bandit(self.state + str(a)))
        ret.dst.reward = self.reward + BAN_ENV.calc_reward(a)
        # logger.map(a=a, r=ret.dst.reward, id=id(ret.dst))
        return ret

    def get_reward(self, depth, player_id, **kw):
        return self.reward

    def get_actions_all(self):
        return list(range(BAN_ENV.K))
