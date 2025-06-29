from typing import List, Dict
import numpy as np
import random
from common.util.export import logger

inf = float("inf")


class Action:
    check_info = None
    reward = None

    def __init__(self, src, action, dst):
        self.action = action
        self.src: State = src
        self.dst: State = dst

    def set_reward(self, reward):
        self.reward = reward
        return self

    def set_value(self, value):
        self.value = value
        return self

    def set_p(self, p):
        self.p = p
        return self

    def get_p_states(self):
        return [[1, self.dst, self.reward]]

    def get_reward(self, **kwargs):
        """ """
        return self.dst.get_reward(**kwargs)

    def get_best_actions(self) -> List["Action"]:
        p = self
        ret = []
        while p:
            ret.append(p)
            p = p.dst.best_action
        return ret

    def get_best_action(self):
        return self.get_best_actions()[-1]

    def __repr__(self):
        return f"action: {self.action}"


class State:
    name = "state"
    parent: "State"
    done = None
    STATE_STORE: Dict[str, "State"] = None

    def __init__(self, state=None, player_id=0, depth=1) -> None:
        self.state = state
        self.depth = depth
        self.player_id = player_id
        self.best_action: Action = None
        self.actions: Dict[str, Action] = None

    def set_best_action(self, a: Action):
        self.best_action = a
        return self

    def set_value(self, v):
        self.value = v
        return self

    @classmethod
    def new_state(cls, key, callback=None) -> "State":
        if cls.STATE_STORE is None:
            cls.STATE_STORE = dict()
        if key not in cls.STATE_STORE:
            if callback is None:
                callback = cls
            cls.STATE_STORE[key] = callback(key)
            # logger.info(cls.STATE_STORE[key])
        return cls.STATE_STORE[key]

    @classmethod
    def all_states(cls) -> List["State"]:
        return [cls.new_state(v) for v in cls.all_state_key()]

    def set_done(self, done):
        self.done = done
        return self

    def set_reward(self, reward):
        self.reward = reward
        return self

    @property
    def op_player_id(self):
        return 1 - self.player_id

    def reset(self):
        return self

    def get_action(self, a) -> Action:
        if self.actions and a in self.actions:
            return self.actions[a]
        return self.gen_action(a)

    def gen_action(self, a):
        raise Exception("tood")

    def get_actions_all(self):
        raise Exception("gg")

    def get_score(self, **kw):
        raise Exception("todo")

    def make_actions(self):
        self.actions = dict()
        for action in self.get_actions_all():
            a = self.get_action(action)
            if a is None:
                continue
            self.actions[action] = a
        return self.actions

    def get_actions(self, **kw) -> Dict[str, Action]:
        if self.done:
            return {}
        if self.actions is not None:
            return self.actions
        return self.make_actions()

    def set_actions(self, actions):
        self.actions = actions
        return self

    def get_random_action(self) -> Action:
        keys = list(self.get_actions().keys())
        k = len(keys)
        if k == 0:
            return None
        return self.actions[keys[np.random.randint(0, k)]]

    def is_game_over(self):
        raise Exception("todo")

    def do(self, action):
        raise Exception(f"{self.__class__}.do not impl")

    def get_regret(self, action):
        raise Exception("todo")

    @property
    def key(self):
        raise Exception("todo")

    @classmethod
    def all_state_key(self):
        raise Exception("todo")

    @classmethod
    def to_str(self):
        raise Exception("todo")

    @classmethod
    def get_init_state(cls):
        raise Exception("todo")

    def get_best_state(self):
        ret = self
        while ret.best_action:
            ret = ret.dst
        return ret

    def dump_best_tree(self, max_depth):
        ret = []

        def dfs(s: State, depth):

            for a in s.get_actions().values():
                if depth == max_depth:
                    ret.append(f'{" "*depth}- {a.action}: {a.get_reward()} {a.reward}')
                else:
                    ret.append(f'{" "*depth}- {a.action}: ')
                    dfs(a.dst, depth + 1)

        dfs(self, 0)
        return "\n".join(ret)

    def get_reward(self, **kw):
        raise Exception("to")

    def get_max_action_reward(self):
        reward = -inf
        for a in self.get_actions().values():
            ar = a.get_reward()
            if ar > reward:
                reward = ar
        return reward

    info = None

    def set_info(self, info):
        self.info = info
        return self

    def __str__(self):
        info = []
        if self.info:
            info.extend(self.info)
        return f"\n".join(
            ["", "-" * 40]
            + [
                f"done:{self.done}, depth:{self.depth}, s:{self.player_id}, reward:{self.get_reward()}",
                f"mask:{self.state}",
                self.to_str(),
                f"{self.best_action}",
            ]
            + info
            + ["-" * 40]
        )
