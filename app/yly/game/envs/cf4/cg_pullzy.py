from common.algo.search.alphabate_search import AlphaBateSearch
from typing import List
import json
import sys
from common.mock import CgMock


class CgMuiltCf4(CgMock):
    uri = "https://www.codingame.com/ide/puzzle/connect-4"
    game_id = "70989246b492bcc523436cf43b6090c82395d392"
    agentsIds = [-1, 4820019]

    def __init__(self):
        C.load(7, 9)
        self.init_state = F4State.new_state(C.INIT_MASK)

    def get_player(self, name=""):
        if name == "ab4":
            return AlphaBateSearch().load(max_depth=4).reset()
        return KagleAgent().reset()

    def replay(self, name="play"):
        path = f"data/cg/cf4/{name}.json"
        player = self.get_player()
        state = self.init_state
        for frame in json.loads(open(path, "r").read())["frames"][1:]:
            if not frame["stdout"]:
                break
            if frame["stdout"][0] == "-":
                continue
            player.search(state)
            logger.info(state)
            a = int(frame["stdout"][:1])
            logger.info(a)
            action = state.get_action(a)
            state = action.dst

    def run(self, **kw):
        player = self.get_player()
        my_id, opp_id = [int(i) for i in self.input().split()]
        # game loop
        state = self.init_state
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
            action = player.search(state)
            # action = state.get_action(opp_previous_action)
            self.debug(
                opp_previous_action=opp_previous_action,
                action=action.action,
                num_valid_actions=num_valid_actions,
            )
            print(action.action)
            state = action.dst


if __name__ == "__main__":
    Solution().run()
