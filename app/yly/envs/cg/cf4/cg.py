from common.algo.search.alphabate_search import AlphaBateSearch
from common.util.export import List, Dict
from common.mock import MockCg
from .model.constant import C
from .model.cf4state import F4State


class CgMuiltCf4(MockCg):
    name = "cf4"
    uri = "https://www.codingame.com/ide/puzzle/connect-4"
    game_id = "70989246b492bcc523436cf43b6090c82395d392"
    agentsIds = [4791004, -1]

    def run(self, **kw):
        player = AlphaBateSearch().load(4, search_type=AlphaBateSearch.AB_MUCH)
        my_id, opp_id = self.ii()
        C.load(1)
        state = F4State.new()
        # game loop
        while True:
            TRUN_INDEX = int(
                self.input()
            )  # starts from 0; As the game progresses, first player gets [0,2,4,...] and second player gets [1,3,5,...]
            board_rows = []
            for i in range(7):
                board_rows.append(
                    self.input()
                )  # one row of the board (from top to bottom)
            num_valid_actions = int(
                self.input()
            )  # number of unfilled columns in the board
            for i in range(num_valid_actions):
                action = int(
                    self.input()
                )  # a valid column index into which a chip can be dropped
            opp_previous_action = int(
                self.input()
            )  # opponent's previous chosen column index (will be -1 for first player in the first turn)
            # player.max_depth = 4 + TRUN_INDEX // 30
            if 0 <= opp_previous_action < C.SHAPES[1][0]:
                state = state.get_action(opp_previous_action).dst
            action = player.search(state)
            # action = state.get_action(opp_previous_action)
            self.log(state=state.state)
            print(action.action)
            state = action.dst


if __name__ == "__main__":
    CgMuiltCf4().run()
