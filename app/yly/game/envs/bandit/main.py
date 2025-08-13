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
        r = BAN_ENV.calc_reward(self.action)
        regret = BAN_ENV.probs[self.action] - BAN_ENV.probs[BAN_ENV.max_idx]
        return regret, r

    def __repr__(self):
        return str(self.action)


class Bandit(State):

    def __init__(self, state="", player_id=0, depth=1):
        super().__init__(state, player_id, depth)

    def get_actions(self, **kw) -> Dict[int, Bction]:
        if self.actions:
            return self.actions
        self.actions = dict()
        for action in range(BAN_ENV.K):
            a = Bction(self, action, self)
            self.actions[action] = a
        return self.actions

    def get_reward(self, actions: List[Bction], **kw):
        return sum([BAN_ENV.calc_reward(v.action) for i, v in enumerate(actions)])

    def __repr__(self):
        return str([v.value for v in self.get_actions().values()])

    def action_size(self):
        return BAN_ENV.K

    def reset_env(self):
        for a in self.get_actions().values():
            a.value = 1
            a.count = 0
            a.tm_value = [1, 1]
        return self
