from common.third_util.np_util import np
import time
import random


from typing import List, Dict
from common.algo.search.state import State, inf, Action
from common.algo.search.param import Params
from collections import deque
from collections import defaultdict
from common.util.export import File, logger, get_log, get_dev_log, progress_bar


def random_seed(v=1):
    logger.info(f"random_seed {v}")
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

    record_dir = "data/test/algo"

    def set_record_dir(self, path):
        self.record_dir = path
        return self

    def get_tmp_file_path(self, name):
        return f"{self.record_dir}/{name}"

    @property
    def logger(self):
        return get_dev_log(self.get_tmp_file_path(self.get_name()))

    def set_name(self, name):
        self.name = name
        return self

    def load(self):
        self.reset()
        return self

    def set_params(self, params):
        self.params: Params = params
        return self

    use_time = 0

    def search(self, state: "State", *args, **kw):
        self.reset()
        start_time = time.time()
        ret = self.search_main(state.reset(), *args, **kw)
        self.use_time = time.time() - start_time
        return ret

    def info(self):
        return []

    def show(self):
        return "\n".join(
            [f"---name:{self.get_name()} use_time:{self.use_time}---"] + self.info()
        )

    def search_main(self, state: "State") -> Action:
        raise Exception("todo")

    def take_action(self, state: "State") -> Action:
        raise Exception("todo")

    def update_action(self, a: Action, *args):
        pass

    def reset(self):
        return self

    def get_name(self):
        return self.name

    def actor(self):
        pass

    def set_train_epoll(self, train_epoll):
        self.train_epoll = train_epoll
        return self

    def train(self, state: State):
        self.reset()
        for i in range(self.train_epoll):
            progress_bar(i + 1, self.train_epoll, msg="train...")
            self.train_one(i, state)

    def train_one(self, i, state: State):
        s = state.reset()
        self.actions = []
        while not s.game_over():
            a = self.take_action(s)
            self.actions.append(a)
            self.update_action(a)
            s = a.get_dst()


class RandomAlgo(Algo):
    def search_main(self, s: State, **kw):
        return s.get_random_action()
