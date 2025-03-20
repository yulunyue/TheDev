from common.algo.manage import SolutionBase, View, logger, MOD, inf

from common.algo.search.mttsearch import MctsSearchTree, MctsNode
from common.algo.search.algo import Algo, np, RandomAlgo
from common.algo.search.alphabate_search import AlphaBateSearch

from collections import defaultdict
from typing import Dict, List
from functools import lru_cache
from app.yly.algo.cg.cf4.constant import C
from app.yly.algo.cg.cf4.f4state import F4State


class Solution(SolutionBase):
    uri = "https://www.codingame.com/ide/puzzle/connect-4"
    game_id = "70989246b492bcc523436cf43b6090c82395d392"
    # log_mode = "debug"
    agentsIds = [4820019, -1]
    name = "f4"
    search_max_depth = 5
    budget = 1000
    max_t = 0.1

    def get_cases(self):
        return [
            # dict(search_type="tree_search",method="analyze"),
            # dict(search_type="alpha_bate_search"),
            # dict(search_type="mcts"),
            dict(
                player1="rand",
                player2="ab",
                depth=self.search_max_depth,
                max_t=self.max_t,
                max_turn=100,
            )
        ]

    def test_all(self, **kw):
        s = F4State(147646293709387072516).init_root()
        self.log(s)

    def get_player(self, search_type) -> Algo:
        return {
            "ts": Algo,
            "ab": AlphaBateSearch,
            "mcts": MctsSearchTree,
            "rand": RandomAlgo,
        }[search_type]()

    def pk(self, player1, player2, nums=1, max_turn=100, **kw):
        players = [self.get_player(player1), self.get_player(player2)]
        for _ in range(nums):
            state = F4State(C.INIT_MASK).init_root()
            i = 0
            while i < max_turn:
                reward = players[i % 2].search(
                    state,
                    depth=self.search_max_depth,
                    # max_t=self.max_t,
                    budget=self.budget,
                )
                self.log(state)
                self.log(players[i % 2])
                if state.best_action is None:
                    break
                state.best_action.reward = reward
                self.log(state.best_action)
                state = state.best_action.dst
                i += 1
            self.log(f"run {i}")

    def replay(self, player1, stdout: List[str], stderr=None, **kw):
        C.TRUN_INDEX = 0
        state = F4State(C.INIT_MASK).init_root()
        search = self.get_player(player1)
        while C.TRUN_INDEX < len(stdout):
            action = state.get_action(int(stdout[C.TRUN_INDEX]))
            alpha = search.search(state, **kw)
            self.log(
                f"put:{state.best_action.key}; num:{search.state_count} best:{alpha}"
            )
            self.log(action)
            state = action.state
            C.TRUN_INDEX += 1

    def exec(self, **kw):
        search, state = AlphaBateSearch(), F4State(C.INIT_MASK).init_root()
        my_id, opp_id = [int(i) for i in self.input().split()]
        # game loop
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
                state: F4State = state.get_action(opp_previous_action).state
            # if my_id==1 and turn_index==1 and 3<=opp_previous_action<=6:
            #     self.output(-2)
            #     continue
            search.search(state, depth=self.search_max_depth)
            self.error(
                opp_previous_action=opp_previous_action,
                # state=str(self.state)
            )
            self.output(state.best_action.key)
            state = state.best_action.state

    def finish(self):
        from common.util.fp import get_cache

        # get_cache(F4State.name).flush()


if __name__ == "__main__":
    np.random.seed(1)
    Solution().run()
