from typing import List, Dict
import numpy as np
import random

inf = float("inf")


class Action:
    info = None
    state_cls = None

    def set_state_cls(self, cls):
        self.state_cls: State = cls
        return self

    def load(self, src, action, dst, reward=0):
        self.action = action
        self.src: State = src
        self.dst: State = dst
        self.reward = reward
        return self

    def __str__(self):
        return f"<Action action:{self.get_action_str()} reward:{self.reward} info:{self.info}>state:{self.src}"

    def set_info(self, info):
        self.info = info
        return self

    def get_action_str(self):
        return self.action

    def get_reward(self, params, **kwargs):
        raise Exception("error")


class State:
    name = "state"
    parent: "State"
    done = None

    def __init__(self, player_id, depth) -> None:
        self.depth = depth
        self.player_id = player_id
        self.best_action: Action = None
        self.actions: Dict[str, Action] = None

    def reset(self):
        return self

    def get_action(self, a) -> Action:
        if self.actions and a in self.actions:
            return self.actions[a]
        return self.gen_action(a)

    def gen_action(self):
        pass

    def get_actions_all(self):
        raise Exception("todo")

    def get_score(self, **kw):
        raise Exception("todo")

    def make_actions(self):
        self.actions = dict()
        for action in self.get_actions_all():
            a = self.get_action(action)
            if a is None:
                continue
            if a.dst.op_done:
                continue
            if a.dst.win_done:
                return {action: a}
            self.actions[action] = a
        return self.actions

    def get_actions(self, depth=1, **kw):
        if depth == 0 or self.done is not None:
            return []
        if self.actions is not None:
            return self.actions
        return self.make_actions()

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
        raise Exception("todo")

    @property
    def win_done(self):
        return False

    @property
    def op_done(self):
        return False
