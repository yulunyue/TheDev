from typing import List, Dict
import numpy as np
import random

inf = float("inf")


class Action:
    WIN_ACTION = 0
    LOSE_ACTION = 1

    def __init__(self, src, action, dst, reward=0):
        self.action = action
        self.src: State = src
        self.dst: State = dst
        self.reward = reward

    def get_states(self):
        return [[1, self.src, self.dst, self.reward]]

    def __str__(self):
        return f"<Action action:{self.action} reward:{self.reward}>"


class State:
    done = -1
    name = "state"

    def __init__(self) -> None:
        self.state = None
        self.depth = 0
        self.best_action: Action = None
        self.actions: List[Action] = None
        self.parent: State = None

    def set_done(self, done):
        self.done = done
        return self

    def reset(self):
        return self

    def get_action(self, *args) -> Action:
        raise Exception("todo")

    def set_depth(self, depth):
        self.depth = depth
        return self

    def calc_value(self, *args):
        raise Exception("todo")

    def get_actions(self, depth=None) -> List[Action]:
        return self.actions

    def set_actions(self, actions):
        self.actions = actions
        return self

    def get_random_action(self) -> Action:
        k = len(self.get_actions())
        if k == 0:
            return None
        return self.actions[np.random.randint(0, k)]

    def is_game_over(self):
        raise Exception("todo")

    def do(self, action):
        raise Exception(f"{self.__class__}.do not impl")

    def get_regret(self, action):
        raise Exception("todo")

    @property
    def key(self):
        raise Exception("todo")

    def new_state(self, *args):
        return self

    def get_cache_done(self, max_search_num=6000, unknow_state=-1, enable_cache=False):
        from common.util.fp import get_cache

        cache = None
        if enable_cache:
            cache = get_cache(self.name)
        self.search_num = 0

        def dfs(s: State):
            self.search_num += 1
            if s.done > unknow_state:
                return s.done, "#"
            actions = s.get_actions()
            if not actions:
                return 0, "#"
            # if cache and cache.exists(s.key):
            #     return cache.get(s.key)
            if self.search_num >= max_search_num:
                return unknow_state, "?"
            op_win = 0
            for a in actions:
                done, acs = dfs(a.dst)
                if done == unknow_state or done == a.src.win_done:
                    return done, str(a.action) + acs
                elif done == a.src.op_done:
                    op_win += 1
            return s.op_done if op_win == len(actions) else 0, str(a.action) + acs

        done, info = dfs(self)
        return done, self.search_num, info

    @property
    def win_done(self):
        raise Exception("todo")

    @property
    def op_done(self):
        raise Exception("todo")
