from common.algo.manage import SolutionBase, View, logger, MOD, inf

from common.algo.search.mttsearch import MctsSearchTree, MctsNode
from common.algo.search.algo import Algo, np, RandomAlgo
from common.algo.search.alphabate_search import AlphaBateSearch, AbSearchIter

from collections import defaultdict
from typing import Dict, List
from functools import lru_cache
from app.yly.algo.cg.cf4.constant import SE, C, StateEnum
from app.yly.algo.cg.cf4.f4state import F4State, S, F4Action


class Solution(SolutionBase):
    uri = "https://www.codingame.com/ide/puzzle/connect-4"
    game_id = "70989246b492bcc523436cf43b6090c82395d392"
    # log_mode = "debug"
    agentsIds = [4820019, -1]
    name = "f4"
    search_max_depth = 5
    budget = 9000
    max_t = 0.1

    def get_search_depth(self, turn):
        return self.search_max_depth

    def get_cases(self):
        return [
            dict(
                player1="ab",
                player2="ab",
                depth=self.search_max_depth,
                max_t=self.max_t,
                max_turn=100,
            )
        ]

    def get_player(self, search_type, param_dyn: StateEnum) -> Algo:
        param_dyn.init_score()
        return {
            "ts": Algo,
            "ai": AbSearchIter,
            "ab": AlphaBateSearch,
            "mcts": MctsSearchTree,
            "rand": RandomAlgo,
        }[search_type]().load(param_dyn=param_dyn)

    def pk(self, player1, player2, nums=1, max_turn=100, **kw):
        players = [self.get_player(player1), self.get_player(player2)]
        data = [[0, 0], [0, 0]]
        for _ in range(nums):
            action = F4Action(None, "init", F4State(C.INIT_MASK).init_root())
            i = 0

            while i < max_turn:
                players[i % 2].search(
                    action,
                    depth=self.search_max_depth,
                    max_t=self.max_t,
                    budget=self.budget,
                )
                data[i % 2][0] = max(data[i % 2][0], players[i % 2].use_time)
                data[i % 2][1] = max(data[i % 2][1], players[i % 2].state_count)
                self.log(action.dst)
                self.log(players[i % 2])
                if action.dst.done > 0 or action.dst.best_action is None:
                    break
                self.log(action.dst.best_action)
                action = action.dst.best_action
                i += 1

            self.log(f"run:{i} win:{players[(i-1)%2]}{S[(i-1)%2]}")
            for i in range(2):
                self.log(
                    f"{players[i].name[:5]} max_use_time:{'%.4f'%data[i][0]} state_count:{data[i][1]}"
                )

    def gene(self, player1, **kw):
        from common.algo.search.gene import Gene

        best_args = (
            Gene()
            .load(
                lambda arg: self.get_player(player1, arg),
                lambda: F4Action(None, "init", F4State(C.INIT_MASK).init_root()),
            )
            .run(SE)
        )
        self.log(best_args)

    def replay(self, player1, stdout: List[str], stderr=None, **kw):
        C.TRUN_INDEX = 0
        state = F4State(C.INIT_MASK).init_root()
        search = self.get_player(player1)
        while C.TRUN_INDEX < len(stdout):
            action = state.get_action(int(stdout[C.TRUN_INDEX]))
            self.log(state)
            if C.TRUN_INDEX % 2 == 1:
                alpha = search.search(
                    state, depth=self.get_search_depth(C.TRUN_INDEX), budget=self.budget
                )
                self.log(search)
                self.log(state.best_action)
            state = action.dst
            C.TRUN_INDEX += 1

    def exec(self, **kw):
        search, state = AbSearchIter(), F4State(C.INIT_MASK).init_root()
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
                state: F4State = state.get_action(opp_previous_action).dst
            # if my_id==1 and turn_index==1 and 3<=opp_previous_action<=6:
            #     self.output(-2)
            #     continue
            depth = self.get_search_depth(C.TRUN_INDEX)
            s_depth = search.search(state, depth=depth, budget=self.budget)
            self.error(
                opp_previous_action=opp_previous_action,
                state_count=search.state_count,
                use_time=search.use_time,
                depth=s_depth,
                # state=str(self.state)
            )
            self.output(state.best_action.action)
            state = state.best_action.dst

    def finish(self):
        from common.util.fp import get_cache

        # get_cache(F4State.name).flush()


if __name__ == "__main__":
    np.random.seed(1)
    Solution().run()
