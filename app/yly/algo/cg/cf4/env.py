from common.algo.manage import SolutionBase, View, MOD, inf, File, get_log

from common.algo.search.mctssearch import MctsSearchTree, MctsNode
from common.algo.search.algo import Algo, np, RandomAlgo
from common.algo.search.alphabate_search import AlphaBateSearch, AbSearchIter

from collections import defaultdict
from typing import Dict, List
from functools import lru_cache
from app.yly.algo.cg.cf4.constant import SE, C, StateEnum, DATA_PATH
from app.yly.algo.cg.cf4.f4state import F4State, S, F4Action, KaggleEnv, board_format


class KagleAgent(Algo):

    def search_main(self, state: F4Action, **kw):
        from app.yly.algo.kagle.c4 import cell_swarm

        state.dst.best_action = state.dst.get_action(
            cell_swarm(*state.dump_to_kaggle())
        )

    def __call__(self, *args, **kwds):
        from app.yly.algo.kagle.c4 import cell_swarm

        return cell_swarm(*args, **kwds)


class Ab(AlphaBateSearch):

    def __call__(self, env: KaggleEnv, conf: KaggleEnv):
        action = F4Action().load_from_kaggle(env, conf)
        self.search(action)
        return action.dst.best_action.action


logger = get_log("cf4")
PLAYERS = dict(
    ab1=lambda: Ab().load(1).set_params(SE),
    ab2=lambda: Ab().load(2).set_params(SE),
    ab3=lambda: Ab().load(3).set_params(SE),
    ab4=lambda: Ab().load(4).set_params(SE),
    ab5=lambda: Ab().load(5).set_params(SE),
    kd1=lambda: KagleAgent().load().set_params(None),
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
            self.actions.append(cur)
            player_id = (player_id + 1) % len(self.players)
        return cur.dst.done - 1

    def run(self, players: List[Algo]):
        self.players = [p.reset() for p in players]
        self.actions: List[F4Action] = []
        if self.env_name == Env.connectx:
            return self.run_kagele()
        return self.run_self()

    def run_kagele(self):
        from common.util.log import JSON_TMP_FILE

        records = self.env.run(self.players)
        JSON_TMP_FILE.write_file(records)
        self.records: List[F4Action] = [
            F4Action().laod_from_karord(
                board=d[0]["observation"]["board"],
                action=d[0]["action"] + d[1]["action"],
            )
            for d in records[1:]
        ]
        step = records[-1][0]["observation"]["step"]
        return -1 if records[-1][0]["reward"] == 0 else (step + 1) % 2

    def render(self, mode=None, **kw):
        if self.env_name == Env.connectx and mode == "html":
            ret = self.env.render(mode=mode, **kw)
            File(f"{DATA_PATH}/{self.env_name}.html").write_file(ret)
        cur = self.state.dst
        for r in self.records:

            logger.info(f"put: {r.action}{S[cur.player_id]} ")
            act = cur.get_action(r.action)
            if not act:
                logger.info("gg")
                break
            cur = act.dst
            f2 = F4State(C.grid_to_mask(r.board)).init_root(C.HEIGHT, C.WIDTH)
            if f2.mask != cur.mask:
                logger.info(f"gbg\n{bin(cur.mask)}\n{bin(f2.mask)}\n" + f2.to_str())
            logger.info(cur.to_str())

    def play(self, name):
        self.get_player(name).search(F4Action(None, None, self.state))
        return self.state.best_action.action
