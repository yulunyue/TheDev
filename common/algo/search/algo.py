import numpy as np
import time
import random

np.set_printoptions(suppress=True, precision=4)
from typing import List, Dict
from common.algo.search.state import State, inf, Action
from common.algo.search.param import Params
from collections import deque
from collections import defaultdict
from common.util.export import File


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
    state_num = 0

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__
        self.params = None

    def set_name(self, name):
        self.name = name
        return self

    def load(self, cache=None, max_t=-1):
        self.cache = cache
        self.max_t = max_t
        self.reset()
        return self

    def time_out(self):
        return self.max_t > 0 and time.time() - self.begin_time >= self.max_t

    def set_params(self, params):
        self.params: Params = params
        return self

    def search(self, state: "State") -> "Action":
        self.begin_time = time.time()
        self.search_main(state.reset())
        self.use_time = int((time.time() - self.begin_time) * 1000)
        return state.get_best_action()

    def search_main(self, state: "State"):
        raise Exception("todo")

    def get_random_action(self, state: State, **kw):
        s = random.random() * state.get_p_sum()
        for a in state.get_actions().values():
            if s <= a.p:
                return a
            s -= a.p

    def get_max_action(self, state: State) -> Action:
        actions = list(state.get_actions().values())
        return actions[np.argmax([a.get_reward() for a in actions])]

    def take_action(self, state: "State") -> Action:
        raise Exception("todo")

    def update_action(self, a: "Action"):
        pass

    def reset(self):
        self.state_num = 0
        return self

    def new_state(self, key):
        pass

    def __str__(self):
        return f"<{self.__class__.__name__}  params:{self.params}>"

    def get_name(self):
        return self.name

    def actor(self):
        pass

    _log = None

    def log(self, msg):
        if self._log is None:
            self._log = File(f"data/algo/log/{self.get_name()}.log").get_writer()
        self._log.write(f"{msg}\n")
        self._log.flush()


class RandomAlgo(Algo):
    def search_main(self, s: State, **kw):
        actions = list(s.get_actions().values())
        if not actions:
            return
        a = np.random.choice(actions)
        s.set_best_action(a)
