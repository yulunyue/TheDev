from common.algo.export import AbState, Action, sigmoid_1_to_1
from .static_state import StateStatic


class C5ACtion(Action):
    src: "StateStatic"
    obs = None
    reward = 0

    def set_obs(self, obs):
        self.reward = 0
        self.obs: dict = obs
        if self.obs.get((self.src.board.in_row, 0)) or self.obs.get(
            (self.src.board.in_row, 1)
        ):
            self.reward = 1
            self.dst.done = self.src.player_id + 1
        return self

    def show(self):
        y, x = self.src.board.get_yx(self.action)
        dst_info = self.dst.state if self.dst else None
        return f"src:{self.src.state}, action:{y},{x},{self.src.board.s(self.src.player_id+1)},r:{self.get_reward()} dst:{dst_info} obs:{self.obs}"
