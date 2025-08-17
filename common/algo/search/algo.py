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
        use_time = int((time.time() - self.begin_time) * 1000)
        self.use_time += use_time
        self.max_use_time = max(self.max_use_time, use_time)
        return state.best_action

    def search_main(self, state: "State"):
        raise Exception("todo")

    def get_max_action(self, state: "State"):
        raise Exception("todo")

    def take_action(self, state: "State") -> Action:
        raise Exception("todo")

    def update_action(self, a: "Action"):
        pass

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
