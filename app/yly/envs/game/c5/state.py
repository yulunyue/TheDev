from common.algo.export import AbState, Action, sigmoid_1_to_1
from common.util.export import List
from .constant import C, CS


class C5ACtion(Action):
    dst: "State"

    def __init__(self, src, action, dst: "State"):
        super().__init__(src, action, dst)
        self.reward = 0
        if self.dst.game_over():
            self.reward = 1
        else:
            reward = 0
            c = 1 if self.src.player_id == 0 else -1
            for i in range(2, C.in_row):
                reward += (i - 1) * 10 * (self.dst.obs[i * c] - self.dst.obs[-i * c])
            self.reward = sigmoid_1_to_1(reward)

    def show(self):
        y, x = self.action // C.width, self.action % C.width
        return f"src:{self.src.state}, action:{y},{x},{C.s(self.src.player_id+1)},r:{self.get_reward()} dst:{self.dst.state}"


class State(AbState):

    def __init__(self, state: int):
        C.set_state(state)
        self.state = state
        self.can_moves = list(C.pos_status[C.STATE_NULL])
        self.obs = C.line_ct.copy()
        self.depth = state.bit_count()
        self.player_id = self.depth % 2
        self.done = None if self.depth != C.size else State.NO_WIN
        if self.obs[C.in_row]:
            self.done = State.FIRST_WIN
        elif self.obs[-C.in_row]:
            self.done = State.SECONEND_WIN
        c = 1 if self.player_id == 0 else -1
        if self.obs[c * (C.in_row - 1)]:
            self.can_moves = [C.get_win_pos(c * (C.in_row - 1))]
        if self.obs[-c * (C.in_row - 1)]:
            self.can_moves = [C.get_win_pos(-c * (C.in_row - 1))]

    def get_action(self, pos):
        state = C.get_next_state(self.state, pos, self.player_id)
        dst = State.new(state)
        a = C5ACtion(self, pos, dst)
        return a

    def make_actions(self):
        actions = []
        for pos in self.can_moves:
            a = self.get_action(pos)
            actions.append(a)
        return actions

    def to_str(self):
        return CS.set_state(self.state).to_str()

    def show_titles(self):
        return f"depth:{self.depth}; player:{self.player_id+1}{C.s(self.player_id+1)}; done:{self.done}"
