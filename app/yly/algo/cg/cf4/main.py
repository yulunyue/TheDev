from common.algo.manage import SolutionBase, View, MOD, inf, File, get_log

from common.algo.search.mctssearch import MctsSearchTree, MctsNode
from common.algo.search.algo import Algo, np, RandomAlgo
from common.algo.search.alphabate_search import AlphaBateSearch, AbSearchIter

from collections import defaultdict
from typing import Dict, List
from functools import lru_cache
from app.yly.algo.cg.cf4.constant import SE, C, StateEnum, DATA_PATH
from app.yly.algo.cg.cf4.f4state import F4State, S, F4Action


def kagle_demo1():
    from app.yly.algo.kagle.c4 import cell_swarm

    return cell_swarm


logger = get_log("cf4")
PLAYERS = dict(
    ab1=lambda: AlphaBateSearch().load(1).set_params(SE),
    ab3=lambda: AlphaBateSearch().load(3).set_params(SE),
    ab5=lambda: AlphaBateSearch().load(5).set_params(SE),
    kd1=lambda: kagle_demo1(),
    negamax="negamax",
)


class Env:
    connectx = "connectx"

    def __init__(self, env_name="connectx", debug=0, height=7, width=9, **kw):
        self.env_name = env_name
        self.debug = debug
        if env_name == Env.connectx:
            from kaggle_environments import make

            self.env = make(env_name, debug=debug, **kw)
            self.state = F4State(None).init_root(
                self.env.configuration.rows, self.env.configuration.columns
            )
            self.env.reset()
        else:
            self.env = self.state = F4State(env_name).init_root(height, width)
            # self.env = self.state

    def get_player(self, k) -> Algo:
        f = PLAYERS[k]()
        if isinstance(f, Algo) and self.env_name == Env.connectx:

            def util(obs, conf):
                a = F4Action(
                    None,
                    None,
                    F4State(obs.board).init_root(
                        conf.rows,
                        conf.columns,
                    ),
                )
                f.search(a)
                if self.debug:
                    a.dst.debug(f"{a.dst.best_action}")
                return a.dst.best_action.action

            return util

        return f

    def run(self, players):
        self.players = [self.get_player(k) for k in players]
        self.actions = []
        if self.env_name == Env.connectx:
            from common.util.log import JSON_TMP_FILE

            records = self.env.run(self.players)
            JSON_TMP_FILE.write_file(records)
            board = []
            bk = "board"
            idx = 0
            for a in records[1:]:
                board.append(f"xxx-[{a[idx]['action']}]-xxx")
                self.actions.append(a[idx]["action"])
                if bk in a[1 - idx]["observation"]:
                    bkv = a[1 - idx]["observation"][bk]
                else:
                    bkv = a[idx]["observation"][bk]
                for h in range(C.HEIGHT):
                    board.append(
                        "".join([str(v) for v in bkv[h * C.WIDTH : (h + 1) * C.WIDTH]])
                    )
                board.append("xxxxxx")
                if a[idx]["status"] == "DONE":
                    return -1 if a[idx]["reward"] == 0 else idx % 2
                idx = 1 - idx
            self.state.debug("msg:\n" + "\n".join(board))
        # else:
        #     self.actions.extend(self.env.run(self.players))

    def render(self, mode=None, **kw):
        if self.env_name == Env.connectx and mode == "html":
            ret = self.env.render(mode=mode, **kw)
            File(f"{DATA_PATH}/{self.env_name}.html").write_file(ret)
        cur = self.state
        for i, a in enumerate(self.actions):
            if not cur:
                logger.info(f"{i} {len(self.actions)}")
                break
            logger.info(f"put: {a}{S[cur.player_id]} ")
            cur = cur.get_action(a).dst
            logger.info(cur.to_str())

    def play(self, name):
        self.get_player(name).search(F4Action(None, None, self.state))
        return self.state.best_action.action


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
