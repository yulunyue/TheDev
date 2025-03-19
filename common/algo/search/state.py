from typing import List, Dict
import numpy as np
import random

inf = float("inf")


class Action:
    def __init__(self, action, state, reward=0):
        self.key = action
        self.state: State = state
        self.reward = reward

    def get_states(self):
        return [[1, self.state, self.reward]]

    def __str__(self):
        return f"<Action key:{self.key} reward:{self.reward}>"


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
                return s.done
            if cache and cache.exists(s.key):
                return cache.get(s.key)
            if self.search_num >= max_search_num:
                return unknow_state
            actions = s.get_actions()
            if not actions:
                return 0
            self_win = op_win = mid_win = un_win = 0
            done = unknow_state
            for a in actions:
                done = dfs(a.state)
                if done == 0:
                    mid_win += 1
                elif done == unknow_state:
                    un_win += 1
                elif done == s.win_done:
                    self_win += 1
                    break
                elif done == s.op_done:
                    op_win += 1
            if self_win:
                done = s.win_done
            elif un_win:
                done = unknow_state
            elif mid_win:
                done = 0
            else:
                done = s.op_done
            if cache and done > unknow_state:
                cache.set(s.key, done)
            return done

        return dfs(self), self.search_num

    @property
    def win_done(self):
        raise Exception("todo")

    @property
    def op_done(self):
        raise Exception("todo")
