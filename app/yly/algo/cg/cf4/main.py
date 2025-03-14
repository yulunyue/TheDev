from common.algo.manage import SolutionBase, View, logger, MOD, inf
from common.algo.search.state import State, Action
from common.algo.search.mttsearch import MctsSearchTree, MctsNode
from common.algo.search.algo import Algo, np
from common.algo.search.alphabate_search import AlphaBateSearch

from collections import defaultdict
from typing import Dict, List
from functools import lru_cache
from app.yly.algo.cg.cf4.constant import C
from app.yly.algo.cg.cf4.f4state import F4State, action_to_str


class Solution(SolutionBase):
    uri = "https://www.codingame.com/ide/puzzle/connect-4"
    game_id = "70989246b492bcc523436cf43b6090c82395d392"
    # log_mode = 'debug'
    agentsIds = [4820019, -1]
    name = "f4"
    search_max_depth = 2
    max_t = 0.1

    def get_cases(self):
        return [
            # dict(search_type="tree_search",method="analyze"),
            # dict(search_type="alpha_bate_search"),
            # dict(search_type="mcts"),
            dict(player1="alpha_bate_search", player2="alpha_bate_search", max_turn=100)
        ]

    def get_player(self, search_type) -> Algo:
        return {
            "tree_search": Algo,
            "alpha_bate_search": AlphaBateSearch,
            "mcts": MctsSearchTree,
        }[search_type]()

    def pk(self, player1, player2, nums=1, max_turn=100, **kw):
        players = [self.get_player(player1), self.get_player(player2)]
        for _ in range(nums):
            state = F4State(C.INIT_MASK).init_root()
            for i in range(max_turn):
                players[i % 2].search(
                    state, depth=1, max_t=self.max_t
                )
                if state.best_action is None:
                    break
                self.log(action_to_str(state.best_action))
                state = state.best_action.state

    def replay(self, stdout: List[str], stderr=None, **kw):
        C.TRUN_INDEX = 0
        state_num = 0
        while C.TRUN_INDEX < len(stdout):
            action = int(stdout[C.TRUN_INDEX])
            self.state: F4State = self.state.put(action)
            self.log(
                "; ".join(
                    [
                        f'round:{C.TRUN_INDEX} {action}{"OX"[C.TRUN_INDEX%2]}',
                        f"search_best_action:{self.state.best_action}",
                        f"state_count:{self.seach.state_count}",
                    ]
                )
            )
            self.seach.search(self.state, self.search_max_depth)
            self.log(self.state)
            state_num += self.seach.state_count
            C.TRUN_INDEX += 1
        self.log(f"round:{C.TRUN_INDEX},state_num:{state_num}")
        self.log(self.state)

    def exec(self, **kw):
        my_id, opp_id = [int(i) for i in self.input().split()]
        # game loop
        self.init()
        while True:
            C.TRUN_INDEX = int(
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
                self.state: F4State = self.state.put(opp_previous_action)
            # if my_id==1 and turn_index==1 and 3<=opp_previous_action<=6:
            #     self.output(-2)
            #     continue
            self.seach.search(self.state, self.search_max_depth)
            self.error(
                opp_previous_action=opp_previous_action,
                # state=str(self.state)
            )
            self.output(self.state.best_action)
            self.state = self.state.next_state[self.state.best_action]


if __name__ == "__main__":
    np.random.seed(1)
    Solution().run()
