from common.algo.export import AbState, Action, sigmoid_1_to_1
from common.util.export import List
from ..board.base_state import BoardC5State, BoardC5


class StateStatic(AbState):
    mode="MAN2"
    @classmethod
    def set_board(cls, w, h, s):
        cls.board = BoardC5().load(w, h, s)
        return cls.new(0).set_state(0)

    def set_state(self, state: int):
        self.board.set_state(state)
        self.state = state
        self.can_moves = list(self.board.can_use)
        depth = state.bit_count()
        self.player_id = self.depth % 2
        return self.set_depth(depth)

    def set_depth(self, depth):
        self.depth = depth
        self.done = None if self.depth != self.board.size else StateStatic.NO_WIN
        return self

    def get_action(self, pos):
        from .static_action import C5ACtion

        state = self.board.get_next_state(self.state, pos, self.player_id)
        obs = self.board.set_state(self.state).put_chess(pos, self.player_id + 1)
        self.board.state = state
        dst: StateStatic = (
            StateStatic.new(state)
            .set_player_id(1 - self.player_id)
            .set_depth(self.depth + 1)
        )
        dst.can_moves = list(self.board.can_use)
        a = C5ACtion(self, pos, dst, obs)
        return a

    def make_actions(self):
        actions = []
        for pos in self.can_moves:
            a = self.get_action(pos)
            actions.append(a)
        return actions

    def to_str(self):

        return (
            BoardC5()
            .load(self.board.width, self.board.height, self.board.in_row)
            .set_state(self.state)
            .to_str()
        )

    def show_titles(self):
        return f"depth:{self.depth}; player:{self.player_id+1}{self.board.s(self.player_id+1)}; done:{self.done}"
