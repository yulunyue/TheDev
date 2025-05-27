from app.yly.algo.cg.cf4.constant import SE, C, StateEnum, DATA_PATH
from app.yly.algo.cg.cf4.cf4state import F4State
from app.yly.algo.cg.cf4.cf4action import F4Action
from common.algo.search.alphabate_search import AlphaBateSearch
from typing import List
import json
import sys


class Solution:
    uri = "https://www.codingame.com/ide/puzzle/connect-4"
    game_id = "70989246b492bcc523436cf43b6090c82395d392"
    agentsIds = [4820019, -1]

    def input(self):
        return input()

    def run(self, **kw):
        search, state = AlphaBateSearch(), F4State.new_state()
        my_id, opp_id = [int(i) for i in self.input().split()]
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

            if 0 <= opp_previous_action < C.WIDTH:
                state = state.get_action(opp_previous_action).dst
            # if my_id==1 and turn_index==1 and 3<=opp_previous_action<=6:
            #     self.output(-2)
            #     continue
            search.search(state, depth=4)
            print(
                json.dumps(
                    dict(
                        opp_previous_action=opp_previous_action,
                        state_count=search.state_count,
                        use_time=search.use_time,
                        # state=str(self.state)
                    )
                ),
                file=sys.stderr,
            )
            print(state.best_action.action)
            state = state.best_action.dst


if __name__ == "__main__":
    Solution().run()
