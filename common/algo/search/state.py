from typing import List, Dict
import numpy as np
import random
from common.util.export import logger, json_dumps, defaultdict

inf = float("inf")


class Action:
    check_info = None
    reward = None

    def __init__(self, src, action, dst=None):
        self.action = action
        self.src: State = src
        self.dst: State = dst
        self.data = dict()

    def get_data(self, key):
        return self.data[key]

    def set_data(self, key, value):
        self.data[key] = value
        return self

    def set_reward(self, reward):
        self.reward = reward
        return self

    def set_value(self, value):
        self.value = value
        return self

    def set_p(self, p):
        self.p = p
        return self

    def do(self, **kw):
        raise Exception("todo")

    def get_p_states(self):
        return [[1, self.dst, self.reward]]

    def get_reward(self, **kwargs):
        raise Exception("todo")

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

    def __init__(self, state=None, player_id=0, depth=0) -> None:
        self.state = state
        self.depth = depth
        self.player_id = player_id
        self.best_action: Action = None
        self.actions: Dict[str, Action] = None

    def get_done(self):
        return self.done

    def set_best_action(self, a: Action):
        self.best_action = a
        return self

    def set_value(self, v):
        self.value = v
        return self

    def set_depth(self, depth):
        self.depth = depth
        return self

    def set_best_action(self, a):
        self.best_action = a
        return self

    def set_done(self, done):
        self.done = done
        return self

    def set_reward(self, reward):
        self.reward = reward
        return self

    def reset(self):
        return self

    def reset_env(self):
        return self

    def get_action(self, a) -> Action:
        actions = self.get_actions()
        if a in self.actions:
            return self.actions[a]
        raise Exception(a, list(actions.keys()))

    def get_score(self, **kw):
        raise Exception("todo")

    def get_actions(self, depth=1, **kw) -> Dict[str, Action]:
        raise Exception("todo")

    def get_random_action(self) -> Action:
        actions = self.get_actions()
        values = list(actions.keys())
        if not values:
            return None
        return values[np.random.randint(0, len(values) - 1)]

    def do(self, action):
        raise Exception(f"{self.__class__}.do not impl")

    def get_regret(self, action):
        raise Exception("todo")

    @property
    def key(self):
        raise Exception("todo")

    def to_str(self):
        return ""

    @classmethod
    def get_init_state(cls):
        raise Exception("todo")

    def dump_tree(self, max_depth):
        ret = []

        def dfs(s: State, depth):
            if s.get_done() or depth == max_depth:
                return s.get_done()
            actions = list(s.get_actions().values())
            for a in actions:
                done = dfs(a.dst, depth + 1)
                ret.append(f'{" "*depth}- {a}: {done}')

        dfs(self, 0)
        ret.reverse()
        return "\n".join(ret)

    def get_reward(self, **kw):
        return 0

    def get_max_action_reward(self):
        reward = -inf
        for a in self.get_actions().values():
            ar = a.get_reward()
            if ar > reward:
                reward = ar
        return reward

    data = None

    def set_data(self, **kw):
        if not self.data:
            self.data = dict()
        self.data.update(kw)
        return self

    def __repr__(self):
        info = []
        if self.data:
            for key, value in self.data.items():
                info.append(f"{key}: {value}")
        return f"\n".join(
            ["", "-" * 40]
            + [
                f"done:{self.done}, depth:{self.depth}, player:{self.player_id}",
                f"mask:{self.state}",
                self.to_str(),
            ]
            + info
            + [f"best_action:\n{self.best_action}", "-" * 40]
        )

    def get_win_player(self):
        return self.done

    def get_depth_reward(self, depth, **kw):
        reward = self.get_reward(**kw)
        return -reward if depth % 2 == 1 else reward
