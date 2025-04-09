from common.algo.manage import SolutionBase, View, MOD, inf, File, get_log

from common.algo.search.mctssearch import MctsSearchTree, MctsNode
from common.algo.search.algo import Algo, np, RandomAlgo
from common.algo.search.alphabate_search import AlphaBateSearch, AbSearchIter

from collections import defaultdict
from typing import Dict, List
from functools import lru_cache
from app.yly.algo.cg.cf4.constant import SE, C, StateEnum, DATA_PATH
from app.yly.algo.cg.cf4.f4state import F4State, S, F4Action


class KagleAgent(Algo):

    def search_main(self, state: F4Action, **kw):
        from app.yly.algo.kagle.c4 import cell_swarm

        state.dst.best_action = state.dst.get_action(
            cell_swarm(*state.dump_to_kaggle())
        )


logger = get_log("cf4")
PLAYERS = dict(
    ab1=lambda: AlphaBateSearch().load(1).set_params(SE),
    ab3=lambda: AlphaBateSearch().load(3).set_params(SE),
    ab5=lambda: AlphaBateSearch().load(5).set_params(SE),
    kd1=lambda: KagleAgent().load(),
    # negamax="negamax",
)


def get_player(k) -> Algo:
    return PLAYERS[k]().set_name(k)


class Env:
    connectx = "connectx"

    def __init__(
        self, env_name=None, init_state=None, debug=0, height=7, width=9, **kw
    ):
        self.env_name = env_name
        self.debug = debug
        if env_name == Env.connectx:
            from kaggle_environments import make

            self.env = make(env_name, debug=debug, **kw)
            self.state = F4Action().load_from_state(
                height=self.env.configuration.rows, width=self.env.configuration.columns
            )
            self.env.reset()
        else:
            self.state = F4Action().load_from_state(height=height, width=width)

    def run_self(self):
        player_id = 0
        cur = self.state
        while cur.dst.done < 0:
            self.players[player_id].search(cur)
            cur = cur.dst.best_action
            self.actions.append(cur.action)
            player_id = (player_id + 1) % len(self.players)
        return cur.dst.done - 1

    def run(self, players):
        self.players = players
        self.actions = []
        if self.env_name == Env.connectx:
            return self.run_kagele()
        return self.run_self()

    def run_kagele(self):
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

    def render(self, mode=None, **kw):
        if self.env_name == Env.connectx and mode == "html":
            ret = self.env.render(mode=mode, **kw)
            File(f"{DATA_PATH}/{self.env_name}.html").write_file(ret)
        cur = self.state.dst
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
