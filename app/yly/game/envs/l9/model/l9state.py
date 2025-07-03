from common.algo.search.state import State
from app.yly.game.envs.l9.model.l9action import L9Action
from app.yly.game.envs.l9.constant import C
from app.yly.game.envs.l9.shape.env import L9ENV
from app.yly.game.envs.l9.shape.chess import Chess
from typing import Dict, List


class L9State(State):
    STATE_STORE: Dict[str, "State"] = dict()
    boards = None

    def set_boards(self, boards):
        self.boards = boards
        return self

    @classmethod
    def new_state(cls, key):
        if key in cls.STATE_STORE:
            return cls.STATE_STORE[key]
        board, depth = key & C.PLACE_MASK2, key >> (C.PLACE_NUM * 2)
        s = L9State(key, player_id=depth % 2 + 1, depth=depth).set_boards(board)
        cls.STATE_STORE[key] = s
        return cls.STATE_STORE[key]

    def get_actions(self, **kw):
        if self.actions:
            return self.actions
        actions = L9ENV.load_from_board(self.boards).get_actions(self.depth)
        self.actions = dict()
        for a in actions:
            key = a.pop("board") + (self.depth + 1) << (C.PLACE_NUM * 2)
            state = L9State.new_state(key)
            action = L9Action(self, state).load(**a)
            self.actions[action.action] = action
        return self.actions

    def to_str(self):
        return L9ENV.print_board(self.boards)
