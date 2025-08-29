from common.third_util.export import PtTable
from .state import StateBase


class Rooms(StateBase):
    def to_str(self):
        def u(i):
            ac = self.get_actions()
            return 0 if i not in ac else ac[i].get_reward()
        idx=self.current_round%2
        p = PtTable().load_from_matrix(
            [
                [f"A{i}" for i in range(6)],
                self.boards[idx],
                self.boards[1-idx][::-1],
                [f"B{5-i}" for i in range(6)],
            ],
            [f"P{5-i}" for i in range(6)],
        )
        return str(p) + f"\nscore:{self.score,self.op_score}"

    def get_action(self, a):
        return super().get_action(int(a))

    def get_win_player(self, rewards, player_idx,*args, **kw):
        if self.reward>1:
            return 1-player_idx
        if self.reward<1:
            return player_idx
        return -1
