from common.mock import CgMock
from common.algo.search.alphabate_search import AlphaBateSearch
from app.yly.game.envs.tic_toc.model.ttstate import TtState
from app.yly.game.envs.tic_toc.constant import C


class TicTocCg(CgMock):
    uri = "https://www.codingame.com/ide/puzzle/tic-tac-toe"
    gameid = "6246186678d52f83e9a2d47885d4b6f60900eed7"
    agentsIds = [
        # 5604295,
        -2,
        -1,
    ]

    def get_search(self):
        return AlphaBateSearch().load(4)

    def run(self):
        s = self.get_search()
        state = TtState.new_state(C.INIT_SATTE)
        while True:
            opponent_row, opponent_col = [int(i) for i in self.input().split()]
            valid_action_count = int(self.input())
            for i in range(valid_action_count):
                row, col = [int(j) for j in self.input().split()]
            if opponent_row != -1 and opponent_col == -1:
                a = C.op_pos(opponent_row,opponent_col)
                state = state.get_action(a).dst
      
            s.search(state)
            b=state.best_action.action
            y,x=C.pos_op(b)
            return f"{y} {x}"


if __name__ == "__main__":
    TicTocCg().run()
