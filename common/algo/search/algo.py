import numpy as np
import time
import random

np.set_printoptions(suppress=True, precision=4)
from typing import List, Dict
from common.algo.search.state import State, inf, Action
from common.algo.search.param import Params
from collections import deque
from collections import defaultdict


def random_seed(v=1):
    np.random.seed(v)
    random.seed(v)


def random_select(states, fn):
    rand, temp = np.random.rand(), 0
    for s in states:
        temp += fn(s)
        if temp > rand:
            return s


class Algo:
    state_count = 0

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__
        self.params = None

    def set_name(self, name):
        self.name = name
        return self

    def load(self, use_cache=False, max_t=-1, num_episodes=1000, epsilon=1):
        self.cache = None
        self.num_episodes = num_episodes
        self.max_t = max_t
        self.epsilon = epsilon
        if use_cache:
            from common.util.export import get_cache

            self.cache = get_cache(self.name)
        self.reset()
        return self

    def time_out(self):
        return self.max_t > 0 and time.time() - self.begin_time >= self.max_t

    def can_epsilon(self):
        return np.random.random() < self.epsilon

    def set_params(self, params):
        self.params: Params = params
        return self

    def search(self, state: "State") -> "Action":
        self.state_count = 0
        self.begin_time = time.time()
        self.search_main(state.reset_env().reset())
        use_time = int((time.time() - self.begin_time) * 1000)
        self.use_time += use_time
        self.max_use_time = max(self.max_use_time, use_time)
        return state.best_action

    def search_main(self, state: State):
        self.rewards_record = []
        self.reward_tmp_all = 0
        for _ in range(self.num_episodes):
            self.run_one(state)
            self.rewards_record.append(self.reward_tmp_all)
        state.set_best_action(self.get_max_action(state))

    def get_max_action(self, state: State):
        raise Exception("todo")

    def run_one(self, state: State):
        raise Exception("todo")

    def reset(self):
        self.max_use_time = 0
        self.use_time = 0
        return self

    def new_state(self, key):
        pass

    def __str__(self):
        return f"<{self.__class__.__name__}  user_time:{self.max_use_time} params:{self.params}>"

    def get_name(self):
        return self.name

    def actor(self):
        pass


class RandomAlgo(Algo):
    def search_main(self, s: State, **kw):
        actions = list(s.get_actions().values())
        if not actions:
            return
        a = np.random.choice(actions)
        s.set_best_action(a)
