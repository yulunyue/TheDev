from common.third_util.np_util import np
import time
import random


from typing import List, Dict
from common.algo.search.state import State, inf, Action, MctsState
from common.algo.search.param import Params
from collections import deque
from collections import defaultdict
from common.util.export import File, logger, get_log


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

    def set_record_dir(self, path):
        self.record_dir = path
        return self

    @property
    def logger(self):
        return get_log(f"{self.record_dir}/algo/{self.name}")

    def set_name(self, name):
        self.name = name
        return self

    def load(self):
        self.reset()
        return self

    def set_params(self, params):
        self.params: Params = params
        return self

    def search(self, state: "MctsState") -> "Action":
        self.reset()
        self.search_main(state.reset())
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

    def debug(self, *args, **kw):
        pass

    def print_best_actions(self, a: Action):
        actions = []
        while a:
            s = a.get_dst()
            actions.append(str(a.action))
            a = s.get_best_action()
        self.logger.debug(
            s.show(
                info=["ab_value:%.10f" % self.get_state_reward(s)],
                title=",".join(actions),
            )
        )

    def get_state_reward(self, s: State):
        return s.get_reward()


class RandomAlgo(Algo):
    def search_main(self, s: State, **kw):
        s.set_best_action(s.get_random_action())
