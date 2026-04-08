from common.algo.export import AbState, Action, sigmoid_1_to_1, Algo
from common.util.export import List, Self
from ..board.base_state import BoardC5State, BoardC5


class ChessState664(AbState):
    init_state = 0
    mode = AbState.MAN2
    env: BoardC5
    w = 6
    h = 6
    in_row = 4
    STATE_STORE = dict()

    @classmethod
    def set_board(cls, state=0) -> "Self":
        board = BoardC5().load(cls.w, cls.h, cls.s).set_state_any(state)
        return cls.new(board.get_state()).set_env(board)

    def set_state(self, state: int):
        self.board.set_state(state)
        self.state = state
        self.can_moves = list(self.board.can_use)
        if isinstance(state, str):
            depth = (state.count("|") + 1) if state else 0
        else:
            depth = state.bit_count()
        self.player_id = self.depth % 2
        return self.set_depth(depth)

    def set_depth(self, depth):
        self.depth = depth
        self.done = None if self.depth != self.env.size else ChessState.NO_WIN
        return self

    def get_action(self, pos):
        from .chess_action import ChessACtion

        state = self.board.get_next_state(self.state, pos, self.player_id)
        obs = self.board.set_state(self.state).put_chess(pos, self.player_id + 1)
        self.board.state = state
        dst: ChessState = (
            ChessState.new(state)
            .set_player_id(1 - self.player_id)
            .set_depth(self.depth + 1)
        )
        dst.can_moves = list(self.board.can_use)
        a = ChessACtion(self, pos, dst).set_obs(obs)
        return a

    def make_actions(self):
        actions = []
        for pos in self.can_moves:
            a = self.get_action(pos)
            actions.append(a)
        return actions

    def to_str(self, algo: Algo = None):
        score = dict()
        if algo is not None:
            for a in self.get_sort_actions():
                score[a.action] = algo.get_action_reward(a)
        return (
            BoardC5()
            .load(
                self.board.width,
                self.board.height,
                self.board.in_row,
                just_for_view=True,
            )
            .set_state(self.state)
            .to_str(score)
        )

    def show_titles(self):
        return f"depth:{self.depth}; player:{self.player_id+1}{self.board.s(self.player_id+1)}; done:{self.done}"


class ChessState333(ChessState):
    w = 3
    h = 3
    in_row = 3
    STATE_STORE = dict()
