import numpy as np
import time

np.set_printoptions(suppress=True, precision=4)
from typing import List
from common.algo.search.state import State, inf, Action
from collections import deque

Env = State


def random_select(states, fn):
    rand, temp = np.random.rand(), 0
    for s in states:
        temp += fn(s)
        if temp > rand:
            return s


class Algo:
    state_count = 0
    _cache = None

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

    def load(self, num_episodes=5000):
        self.num_episodes = num_episodes
        return self

    def run_one_step(self, episode, action, r):
        return 0

    def search_main(self, state, **kw):
        pass

    def search(self, state: State, **kw):
        state.best_action = None
        self.state_count = 0
        self.begin_time = time.time()
        ret = self.search_main(state, **kw)
        self.use_time = time.time() - self.begin_time
        return ret

    def run(self, state: State):
        self.regrets_record = []
        self.rewards_record = []
        regret = 0
        reword = 0
        for episode in range(self.num_episodes):
            action = state.get_action(episode)
            r = state.do(action)
            reword += r
            regret += self.run_one_step(episode, r, state, action)
            self.rewards_record.append(reword)
            self.regrets_record.append(regret)
            if action.state.done:
                break
            state = action.state
        return self

    def new_state(self, key):
        pass

    def __str__(self):
        return f"<{self.__class__.__name__} state_all:{self.state_count} user_time:{'%.3f'%self.use_time}>"


class Baoli(Algo):

    def search_main(self, state: State, depth=0, **kw):
        mvs: List[State] = state.get_actions(depth=depth, **kw)
        self.state_count += 1
        if not mvs:
            return state.calc_value(depth=depth, **kw)
        state.value = -inf
        for action, next_state in mvs:
            value = -self.search_main(next_state, depth - 1)
            if value > state.value:
                state.value = value
                state.best_action = action
        return state.value


class RandomAlgo(Algo):
    def search_main(self, state, **kw):
        actions = state.get_actions()
        if actions:
            state.best_action = np.random.choice(actions)
