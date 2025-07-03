from common.algo.search.state import State
from app.yly.game.envs.l9.model.l9action import L9Action
from app.yly.game.envs.l9.constant import C
from app.yly.game.envs.l9.shape.env import L9ENV
from app.yly.game.envs.l9.shape.chess import Chess
from typing import Dict, List


class L9State(State):
    STATE_STORE: Dict[str, "State"] = None

    @classmethod
    def new_state(cls, key):
        if key in cls.STATE_STORE:
            return cls.STATE_STORE[key]
        if isinstance(key, str):
            boards = [int(v) for v in key[:24]]
            depth = int(key[24:])
            actions = L9ENV
            cls.STATE_STORE[key] = L9State(key, player_id=depth % 2, depth=depth)
        return cls.STATE_STORE[key]

    def gen_action(self, a):
        a = L9Action(self, a)
