from common.third_util.export import PtTable
from .state import StateBase


class Rooms(StateBase):
    def to_str(self):
        def u(i):
            ac = self.get_actions()
            return 0 if i not in ac else ac[i].get_reward()

        p = PtTable().load_from_matrix(
            [
                [f"A{i}" for i in range(6)],
                self.boards if self.current_round % 2 else self.op_boards,
                self.op_boards[::-1] if self.current_round % 2 else self.boards[::-1],
                [f"B{5-i}" for i in range(6)],
            ],
            [f"P{5-i}" for i in range(6)],
        )
        return str(p) + f"\nscore:{self.score,self.op_score}\n"

    def get_win_player(self, rewards, *args, **kw):
        if rewards[-1][0] < rewards[-1][1]:
            return 1
        if rewards[-1][0] > rewards[-1][1]:
            return 0
        return -1

    @staticmethod
    def new(state) -> "Rooms":
        if state not in Rooms.STATE_MAP:
            Rooms.STATE_MAP[state] = Rooms(state)
        return Rooms.STATE_MAP[state]
