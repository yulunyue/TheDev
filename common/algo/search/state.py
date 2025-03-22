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

    @property
    def win_done(self):
        raise Exception("todo")

    @property
    def op_done(self):
        raise Exception("todo")
