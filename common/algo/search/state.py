from typing import List, Dict
import numpy as np
import random
from common.util.export import logger, json_dumps, defaultdict
from .param import Params, Param

inf = float("inf")


class Action:
    check_info = None
    reward = None
    regret = 0

    def __init__(self, src, action, dst=None):
        self.action = action
        self.src: State = src
        self.dst: State = dst
        self.data = dict()

    def get_regret(self):
        return self.regret

    @property
    def key(self):
        return f"{self.src.state}_{self.action}"

    def get_dst(self):
        return self.dst

    def get_data(self, key, default_value):
        return self.data.get(key, default_value)

    def set_data(self, key, value):
        self.data[key] = value
        return self

    def set_p(self, p):
        self.p = p
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
        return f"action: {self.action}, reward: {self.reward}, data:{self.data}"


class State:
    name = "state"
    parent: "State"
    done = None
    STATE_STORE: Dict[str, "State"] = None

    def __init__(self, state=None, player_id=0, depth=0) -> None:
        self.state = state
        self.depth = depth
        self.data = dict()
        self.player_id = player_id
        self.best_action: Action = None
        self.actions: Dict[str, Action] = None

    @classmethod
    def new(cls, state=None, **kw):
        if cls.STATE_STORE is None:
            cls.STATE_STORE = dict()
        if state not in cls.STATE_STORE:
            cls.STATE_STORE[state] = cls(state, **kw)
        return cls.STATE_STORE[state]

    def get_done(self):
        return self.done

    def action_size(self):
        raise Exception("tood")

    def set_best_action(self, a: Action):
        self.best_action = a
        return self

    def set_depth(self, depth):
        self.depth = depth
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

    def get_steps(self, steps) -> List["State"]:
        ret = [self]
        s = self
        for step in steps:
            action = s.get_action(step)
            s = action.get_dst()
            ret.append(s)
        return ret

    def get_seq_score_forward(self, states: List["State"], gamma=0.5):
        """
        计算一个序列的价值, 未来的值更重要
        """
        ret = 0
        for a in states:
            ret = gamma * ret + a.get_reward()
        return ret

    def get_seq_score_backward(self, states: List["State"], gamma=0.5):
        """
        计算一个序列的价值，当前值更重要
        """
        return self.get_seq_score_forward(states[::-1], gamma)

    def get_bellman_score(self, gamma=0.5):
        ret = self.get_reward()
        for a in self.get_actions().values():
            ret += gamma * a.get_reward() * a.p
        return ret

    def get_actions(self, depth=1, **kw) -> Dict[str, Action]:
        if self.get_done():
            return dict()
        if self.actions is not None:
            return self.actions
        self.actions = self.make_actions()
        return self.actions

    def make_actions(self):
        raise Exception("todo")

    def get_random_action(self) -> Action:
        actions = self.get_actions()
        values = list(actions.keys())
        if not values:
            return None
        return actions[np.random.randint(0, len(values) - 1)]

    def to_str(self):
        return ""

    def bfs(self) -> Dict[str, "State"]:
        ret = {self.state: self}
        q = [self]
        while q:
            t = q
            q = []
            for s in t:
                for a in s.get_actions().values():
                    d = a.get_dst()
                    if d.state in ret:
                        continue
                    ret[d.state] = d
                    q.append(d)
        return ret

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

    def get_reward(self, actions: List[Action] = None, params: Params = None) -> int:
        return self.reward

    def get_self_reward(self, actions: List[Action], params: Params = None):
        return self.get_reward(actions, params=params)

    def get_max_action_reward(self):
        reward = -inf
        for a in self.get_actions().values():
            ar = a.get_reward()
            if ar > reward:
                reward = ar
        return reward

    def set_data(self, **kw):
        self.data.update(kw)
        return self

    def __repr__(self):
        return f"\n".join(
            ["", "-" * 40]
            + [
                f"done:{self.done}, depth:{self.depth}, player:{self.player_id}",
                f"mask:{self.state}",
                self.to_str(),
                f"info:{self.data}",
            ]
            + [f"best_action:\n{self.best_action}", "-" * 40]
        )

    def get_win_player(self, *args, **kw):
        return self.done
