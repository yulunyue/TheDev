from common.algo.search.state import State
from app.yly.envs.cg.l9.model.l9action import L9Action
from app.yly.envs.cg.l9.constant import C
from app.yly.envs.cg.l9.shape.env import L9ENV
from app.yly.envs.cg.l9.shape.chess import Chess
from typing import Dict, List


class L9State(State):
    STATE_STORE: Dict[str, "State"] = dict()

    def set_state(self, board, place_move):
        self.board = board
        self.place_move = place_move
        return self

    @classmethod
    def new_state(cls, key) -> "L9State":
        if key in cls.STATE_STORE:
            return cls.STATE_STORE[key]
        board, player_state = key & C.PLACE_MASK2, key >> (C.PLACE_NUM * 2)
        s = L9State(key, player_id=(player_state & 1) + 1).set_state(
            board, player_state >> 1
        )
        cls.STATE_STORE[key] = s
        return cls.STATE_STORE[key]

    def get_actions(self, **kw) -> Dict[str, L9Action]:
        if self.actions:
            return self.actions
        actions = L9ENV.load_from_board(self.board).get_actions(
            self.player_id, self.place_move
        )
        if len(actions) == 0:
            self.set_done(self.player_id)
            return {}
        self.actions = dict()
        for a in actions:
            place_move = self.place_move
            if place_move >= 1:
                place_move -= 1
            key = (2 * place_move + 2 - self.player_id) << (C.PLACE_NUM * 2)
            s = L9State.new_state(a["board"] + key).set_done(a["done"])
            action = L9Action(self, s).load(**a)
            self.actions[action.action] = action
        return self.actions

    def get_action(self, a):
        return self.get_actions()[a]

    def to_str(self):
        from ..api import ApiAlgo

        ApiAlgo().search_main(self)
        actions = list(self.get_actions().values())
        return "\n".join(
            [
                f"place_move: {self.place_move}, actions: {len(actions)}",
                L9ENV.print_board(self.board),
            ]
            + [str(a) for i, a in enumerate(actions)]
        )
