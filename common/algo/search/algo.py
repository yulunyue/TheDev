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

    def search(self, state: State, use_cache=None, state_max_num=-1, depth=0, **kw):
        from common.util.fp import get_cache

        cache = get_cache(self.name) if use_cache else None
        self.state_clear(state)
        self.state_count = 0
        self.state_max_num = state_max_num
        self.begin_time = time.time()
        ret = self.search_main(state, cache=cache, depth=depth, **kw)
        self.use_time = time.time() - self.begin_time
        return ret

    def state_clear(self, state: State):
        state.best_action = None

    def new_state(self, key):
        pass

    def __str__(self):
        return f"<{self.__class__.__name__} state_all:{self.state_count} user_time:{'%.3f'%self.use_time}>"


class RunAlgo(Algo):
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


class Baoli(Algo):

    def state_clear(self, state: State):
        pass

    def search_main(self, state: State, depth=0, cache=None, **kw):
        actions: List[Action] = state.get_actions(depth=depth, **kw)
        self.state_count += 1
        if self.state_count >= self.state_max_num:
            return None
        if not actions or depth == 0:
            return state.calc_value(tp="baoli")
        best = -inf
        for a in actions:
            value = self.search_main(a.dst, depth - 1, cache=cache)
            if value is None:
                return None
            value = -value
            if value > best:
                best = value
        return best

class SearchBfs(Baoli):
    def search_main(self, state, depth=0, cache=None, **kw):
        q=[state]
        while q and self.state_count<self.state_max_num:
            s=q
            q=[]
            for v in s:
                for n in v.get_actions():
                    q.append(v)
                self.state_count+=1
        

class RandomAlgo(Algo):
    def search_main(self, state: State, **kw):
        actions = state.get_actions()
        if actions:
            state.best_action = np.random.choice(actions)
