from app.yly.algo.cg.cf4.constant import SE, C, StateEnum, DATA_PATH
from app.yly.algo.cg.cf4.f4state import F4State, S, F4Action
from common.algo.manage import SolutionBase, View, MOD, inf, File, get_log
from typing import List


class Solution(SolutionBase):
    uri = "https://www.codingame.com/ide/puzzle/connect-4"
    game_id = "70989246b492bcc523436cf43b6090c82395d392"
    # log_mode = "debug"
    agentsIds = [4820019, -1]
    name = "f4"
    search_max_depth = 4
    budget = 9000
    max_t = 0.1

    def evaluate_fitness(
        self, gene: StateEnum, opponents: List[StateEnum] = None, num_games=4, **kw
    ):
        wins = 0
        if not opponents:
            opponents = [SE]
        for op_gene in opponents:
            for _ in range(num_games):
                result1 = self.simulate_match(
                    gene, op_gene=op_gene, first_player=0, **kw
                )
                result2 = self.simulate_match(
                    gene, op_gene=op_gene, first_player=1, **kw
                )
                wins += result1 + result2
        return wins / (len(opponents) * num_games * 2)

    def simulate_match(
        self,
        gene: StateEnum,
        player1=None,
        player2=None,
        op_gene: StateEnum = None,
        first_player=0,
        **kw,
    ):
        action = self.get_init_action()
        ais: List[Algo] = [
            self.get_player(gene, search_type=player1),
            self.get_player(op_gene, search_type=player2),
        ]
        cur_player = first_player
        while action.dst.done < 0:
            ais[cur_player].search(action)
            action = action.dst.best_action
            cur_player = 1 - cur_player
        if action.dst.done == 1:
            ret = 1 if first_player == 0 else 0
        elif action.dst.done == 2:
            ret = 0 if first_player == 0 else 1
        else:
            ret = 0.5
        logger.info(f"\n [{ais[first_player]}] \npk {ret}\n [{ais[1-first_player]}]")
        logger.info(f"\n{action.dst}")
        return ret

    def get_search_depth(self, turn):
        return self.search_max_depth

    def get_cases(self):
        return [
            dict(
                player1="ab1",
                player2="mcts",
            )
        ]

    def pk(self, player1, player2, nums=1, max_turn=100, **kw):
        players = [
            self.get_player(SE, search_type=player1),
            self.get_player(SE, search_type=player2),
        ]
        data = [[0, 0], [0, 0]]
        for _ in range(nums):
            action = self.get_init_action()
            i = 0
            while i < max_turn:
                players[i % 2].search(action)
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

    def gene(self, player1, tp="s", **kw):
        from common.algo.search.gene import Gene
        from common.algo.search.se import SeOptimize

        best_args = (
            dict(g=Gene, s=SeOptimize)[tp]().load(self.evaluate_fitness).run(SE, **kw)
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

    def ln(self, **kw):
        # from common.algo.learn.ln import Ln
        from common.algo.learn.dqn import Dqn
        from torch import nn

        class Md(nn.Module):
            def __init__(self):
                super().__init__()
                self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
                self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
                self.fc = nn.Linear(64 * 6 * 7, 7)  # 输出7个动作的Q值

            def forward(self, x):
                x = nn.functional.relu(self.conv1(x))
                x = nn.functional.relu(self.conv2(x))
                x = x.view(x.size(0), -1)
                return self.fc(x)

        self.log(
            Dqn()
            .load(env_init_fun=lambda: self.get_init_action().dst, model_fun=Md)
            .train()
        )

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


if __name__ == "__main__":
    np.random.seed(1)
    Solution().run()
