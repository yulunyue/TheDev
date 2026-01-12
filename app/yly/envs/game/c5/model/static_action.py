from common.algo.export import AbState, Action, sigmoid_1_to_1
from .static_state import StateStatic


class C5ACtion(Action):
    src: "StateStatic"
    reward = 0

    def get_dst2(self):
        if self.dst is not None:
            return self.dst
        b = self.src.board
        state = b.get_next_state(self.src.state, self.action, self.src.player_id)
        obs = b.set_state(self.src.state).put_chess(self.action, self.src.player_id + 1)
        # self.board.change_chess_statu(pos, 0)
        dst: StateStatic = (
            StateStatic.new(state)
            .set_player_id(1 - self.src.player_id)
            .set_depth(self.src.depth + 1)
        )
        dst.can_moves = list(b.can_use)
        self.reward = 0
        self.obs: dict = obs

        if self.obs.get((self.dst.board.in_row, 0)) or self.obs.get(
            (self.dst.board.in_row, 1)
        ):
            self.reward = 1
            dst.done = self.src.player_id + 1
        # else:
        #     reward = 0
        #     c = 1 if self.src.player_id == 0 else -1
        #     for i in range(2, dst.board.in_row):
        #         reward += (i - 1) * 10 * (self.dst.obs[i * c] - self.dst.obs[-i * c])
        #     self.reward = sigmoid_1_to_1(reward)
        self.dst = dst
        return self.dst

    def show(self):
        self.obs = dict()
        y, x = self.src.board.get_yx(self.action)
        return f"src:{self.src.state}, action:{y},{x},{self.src.board.s(self.src.player_id+1)},r:{self.get_reward()} dst:{self.dst.state} obs:{dict(self.obs)}"
