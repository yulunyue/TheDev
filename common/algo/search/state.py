from typing import List, Dict
import numpy as np
import random
from common.util.export import logger

inf = float("inf")


class Action:
    info = None
    check_info = None

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

    def __str__(self):
        return f"\n".join(
            [
                f"<Action action:{self.get_action_str()} reward:{self.get_reward()}>",
                f"{self.src}",
            ]
        )

    def get_p_states(self):
        return [[1, self.dst, self.reward]]

    def set_info(self, info):
        self.info = info
        return self

    def get_action_str(self):
        return self.action

    def get_reward(self, **kwargs):
        return 0


class State:
    name = "state"
    parent: "State"
    done = None
    STATE_STORE: Dict[str, "State"] = None

    def __init__(self, state, player_id=0, depth=1) -> None:
        self.state = state
        self.depth = depth
        self.player_id = player_id
        self.best_action: Action = None
        self.actions: Dict[str, Action] = None

    # def __str__(self):
    #     return f"state:{self.state}"

    def set_value(self, v):
        self.value = v
        return self

    def get_reward(self):
        raise Exception("todo")

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

    def get_actions(self, depth=1, **kw) -> Dict[str, Action]:
        if depth == 0 or self.done:
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
