import numpy as np

np.set_printoptions(suppress=True, precision=4)
from typing import List
from .state import State, inf, Action
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

    def get_cache(self):
        if self._cache is None:
            from common.util.fp import Cache

            self._cache = Cache(self.name)
        return self._cache

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

    def load(self, num_episodes=5000):
        self.num_episodes = num_episodes
        return self

    def search_main(self, state: State, depth=0):
        mvs: List[State] = state.get_nexts(depth)
        self.state_count += 1
        if not mvs:
            return state.calc_value(depth)
        state.value = -inf
        for action, next_state in mvs:
            value = -self.search_main(next_state, depth - 1)
            if value > state.value:
                state.value = value
                state.best_action = action
        return state.value

    def search_bfs_in_db(self, env: State, max_num=1000):
        q = deque([env])
        while q and max_num > 0:
            c = q.popleft()
            if 1:
                pass
            for d in c.get_nexts():
                q.append(d)
            max_num -= 1

    def get_action(self, episode):
        return self.env.get_action(episode)

    def run_one_step(self, episode, action, r):
        return 0

    def search(self, state: State, depth):
        state.best_action = None
        self.state_count = 0
        return self.search_main(state, depth)

    def self_play(self, state: State):
        while not state.is_game_over():
            pass

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
