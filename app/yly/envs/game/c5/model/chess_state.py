from common.algo.export import AbState, Action, sigmoid_1_to_1, Algo
from common.util.export import List, Self
from ..board.base import BoardC5, format


class CState664(AbState):
    init_state = 0
    mode = AbState.MAN2
    env: BoardC5
    w = 6
    h = 6
    in_row = 4
    STATE_STORE = dict()
    name = "C664"

    @classmethod
    def set_board(cls, state=0) -> "Self":
        board = BoardC5().load(cls.w, cls.h, cls.in_row).set_state_any(state)
        return cls.new(board.get_state()).set_env(board)

    def set_env(self, env):
        self.env = env
        self.board = env
        return self

    def set_state(self, state: int):
        self.board.set_state(state)
        self.state = state
        self.can_moves = self.get_can_moves()
        if isinstance(state, str):
            depth = (state.count("|") + 1) if state else 0
        else:
            depth = state.bit_count()
        self.player_id = depth % 2
        return self.set_depth(depth)

    def set_depth(self, depth):
        self.depth = depth
        self.done = None if self.depth != self.env.size else CState664.NO_WIN
        return self

    def get_action(self, pos):
        from .chess_action import ChessACtion

        obs = self.board.set_state(self.state).put_chess(pos, self.player_id + 1)
        new_state = self.board.get_state()
        dst: CState664 = (
            CState664.new(new_state)
            .set_env(self.board)
            .set_player_id(1 - self.player_id)
            .set_depth(self.depth + 1)
        )
        dst.state = new_state
        dst.can_moves = dst.get_can_moves()
        a = ChessACtion(self, pos, dst).set_obs(obs)
        return a

    def get_can_moves(self):
        can_move = self.board.mask_full ^ self.board.state_pos
        moves = []
        while can_move:
            low_bit = can_move & -can_move
            idx = int(low_bit.bit_length() - 1)
            moves.append(idx)
            can_move ^= low_bit
        return moves

    def make_actions(self):
        actions = []
        self.board.set_state(self.state)
        self.can_moves = self.get_can_moves()
        for pos in self.can_moves:
            a = self.get_action(pos)
            actions.append(a)
        return actions

    def to_str(self, algo: Algo = None):
        return [
            BoardC5().load(self.w, self.h, self.in_row).set_state(self.state).to_str()
        ]

    def show_titles(self):
        return f"depth:{self.depth}; player:{self.player_id+1}{format(self.player_id+1)}; done:{self.done}"
