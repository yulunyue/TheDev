from common.algo.export import State
from app.yly.game.envs.tic_toc.shape.env import E, C
from app.yly.game.envs.tic_toc.model.ttaction import TtAction
from typing import List, Dict


class TtState(State):
    STATE_STORE: Dict[int, "TtState"] = dict()

    def __init__(self, state, board, last_pos, player_id=0, depth=0):
        super().__init__(state, player_id, depth)
        self.board: int = board
        self.last_pos = last_pos

    @staticmethod
    def new_state(key):
        if key in TtState.STATE_STORE:
            return TtState.STATE_STORE[key]
        board, player_id, last_pos = C.decode_state(key)
        TtState.STATE_STORE[key] = TtState(key, board, last_pos, player_id=player_id)
        return TtState.STATE_STORE[key]

    def get_actions(self, depth=1, **kw):
        if self.actions:
            return self.actions
        self.actions = dict()
        e = E.set_state(self.board)
        self.set_done(e.value)
        actions = e.get_actions(self.last_pos)
        for a in actions:
            k = C.encode_state(self.board, self.player_id, a["pos1"], a["pos2"])
            ac = TtAction(
                self,
                a["pos1"] * 9 + a["pos2"],
                TtState.new_state(k).set_depth(self.depth + 1),
            )
            self.actions[ac.action] = ac
        return self.actions

    def get_action(self, a):
        actions = self.get_actions()
        if a in actions:
            return actions[a]
        raise Exception(a, list(actions.keys()))

    def to_str(self):
        return E.to_str(
            self.board,
            f"last_pos:{self.last_pos}, actions:{len(self.get_actions().keys())}",
        )

    def __repr__(self):
        # self.get_actions()
        return super().__repr__()

    def get_win_player(self):
        if self.done == 1 or self.done == 2:
            return self.done
        return None
