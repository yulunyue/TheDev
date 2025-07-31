from typing import List, Dict
import numpy as np
import random
from common.util.export import logger, json_dumps, defaultdict

inf = float("inf")


class Action:
    check_info = None
    reward = None
    data = None

    def __init__(self, src, action, dst=None):
        self.action = action
        self.src: State = src
        self.dst: State = dst

    def get_data(self, key):
        return self.data[key]

    def set_data(self, key, value):
        if not self.data:
            self.data = dict()
        self.data[key] = value
        return self

    def set_reward(self, reward):
        self.reward = reward
        return self

    def get_reward(self, **kwargs):
        return self.reward

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
        return f"action: {self.action}, reward: {self.reward}"


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

    def action_size(self):
        raise Exception("tood")

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
        return actions[np.random.randint(0, len(values) - 1)]

    def do(self, action):
        raise Exception(f"{self.__class__}.do not impl")

    def get_regret(self, action):
        raise Exception("todo")

    def to_str(self):
        return ""

    @classmethod
    def get_init_state(cls):
        raise Exception("todo")

    def dump_tree(self, max_depth):
        ret = []

        def dfs(s: State, depth, stacks):
            if s.get_done() or depth == max_depth:
                return s.get_done()
            actions = list(s.get_actions().values())
            for a in actions:
                done = dfs(a.dst, depth + 1, stacks + [a])
                ret.append(
                    f'{" "*depth}- {a}: reward:{a.dst.get_reward(actions=stacks)}, down:{done}'
                )

        dfs(self, 0, [])
        ret.reverse()
        return "\n" + "\n".join(ret)

    def get_reward(self, *args, **kw) -> int:
        raise Exception("todo", args, kw)

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

    def get_win_player(self, *args, **kw):
        return self.done
