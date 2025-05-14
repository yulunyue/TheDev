import numpy as np
import time
import random

np.set_printoptions(suppress=True, precision=4)
from typing import List
from common.algo.search.state import State, inf, Action
from common.algo.search.param import Params
from collections import deque

Env = State


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

    def set_name(self, name):
        self.name = name
        return self

    def load(self, use_cache=False, max_t=-1, num_episodes=1000):

        self.cache = None
        self.num_episodes = num_episodes
        self.max_t = max_t
        if use_cache:
            from common.util.fp import get_cache

            self.cache = get_cache(self.name)
        return self

    def set_params(self, params):
        self.params: Params = params
        return self

    def search_main(self, state, **kw):
        pass

    def set_env_cls(self, cls):
        self.env_cls = cls
        return self

    def search(self, *args) -> Action:
        action: Action = self.env_cls(*args)
        self.state_count = 0
        self.begin_time = time.time()
        self.search_main(action)
        use_time = int((time.time() - self.begin_time) * 1000)
        self.use_time += use_time
        self.max_use_time = max(self.max_use_time, use_time)
        return action.dst.best_action

    def reset(self):
        self.max_use_time = 0
        self.use_time = 0
        return self

    def new_state(self, key):
        pass

    def __str__(self):
        return f"<{self.__class__.__name__}  user_time:{self.max_use_time} params:{self.params}>"


class RunAlgo(Algo):
    def run_one_step(self, episode, action, r):
        return 0

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
    def search_dfs(self, s: Action, depth):
        actions: List[Action] = s.dst.get_actions(depth=depth)
        if not actions or depth == 0:
            return s.get_reward()
        self.state_count += 1
        if self.state_count >= self.state_max_num:
            return None
        best = -inf
        cur_done = s.dst.player_id
        for a in actions:
            done, value = self.search_dfs(a, depth - 1)
            if done==a.dst.player_id:
                return done,value
            elif done==-1:
                cur_done=-1
            value = -value
            if value > best:
                best = value
        return cur_done,best

    def search_dfs_main(self,cur:Action,max_depth=6,state_max_num=3000):
        self.begin_time=time.time()
        self.state_count=0
        self.state_max_num=state_max_num
        done,value=self.search_bfs(cur,max_depth)
        return dict(done=done)

    def search_bfs(self, state, depth=0, cache=None, **kw):
        q = [state]
        while q and self.state_count < self.state_max_num:
            s = q
            q = []
            for v in s:
                for n in v.get_actions():
                    q.append(v)
                self.state_count += 1


class RandomAlgo(Algo):
    def search_main(self, a: Action, **kw):
        actions = a.dst.get_actions()
        if actions:
            a.dst.best_action = np.random.choice(actions)
