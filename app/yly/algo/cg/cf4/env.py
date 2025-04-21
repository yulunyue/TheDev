from common.algo.manage import SolutionBase, View, MOD, inf, File, get_log

from common.algo.search.mctssearch import MctsSearchTree, MctsNode
from common.algo.search.algo import Algo, np, RandomAlgo
from common.algo.search.alphabate_search import AlphaBateSearch, AbSearchIter

from collections import defaultdict
from typing import Dict, List
from functools import lru_cache
from app.yly.algo.cg.cf4.constant import SE, C, StateEnum, DATA_PATH, S
from app.yly.algo.cg.cf4.states.f4action import F4Action, get_action
from app.yly.algo.cg.cf4.kagle import Kagle, KagleAgent, KaggleEnv


class Ab(AlphaBateSearch):

    def __call__(self, env: KaggleEnv, conf: KaggleEnv):
        action = F4Action().load_from_kaggle(env, conf)
        self.search(action)
        return action.dst.best_action.action


logger = get_log("cf4")
PLAYERS = dict(
    ab1=lambda: Ab().load(1).set_params(SE).set_env_cls(get_action),
    ab2=lambda: Ab().load(2).set_params(SE).set_env_cls(get_action),
    ab3=lambda: Ab().load(3).set_params(SE).set_env_cls(get_action),
    ab4=lambda: Ab().load(4).set_params(SE).set_env_cls(get_action),
    ab5=lambda: Ab().load(5).set_params(SE).set_env_cls(get_action),
    kd1=lambda: KagleAgent().load().set_params(None).set_env_cls(get_action),
    kd2=lambda: Kagle().load().set_params(None).set_env_cls(get_action),
    # negamax="negamax",
)


def get_player(k) -> Algo:
    return PLAYERS[k]().set_name(k).reset()


class Env:
    connectx = "connectx"

    def __init__(self, env_name=None, debug=0, height=7, width=9, **kw):
        self.env_name = env_name
        self.debug = debug
        self.width = width
        self.height = height
        self.init_state = None
        if env_name == Env.connectx:
            from kaggle_environments import make

            self.env = make(env_name, debug=debug, **kw)
            self.width = self.env.configuration.rows
            self.height = self.env.configuration.columns
            self.env.reset()
        else:
            self.env = None
        C.load(h=self.height, w=self.width)

    def run_self(self, state=None):
        player_id = 0
        while True:
            state = self.players[player_id].search(state)
            if state is None:
                return
            self.records.append(state)
            player_id = (player_id + 1) % len(self.players)

    def run(self, players: List[Algo], state=None):
        self.players = [p.reset() for p in players]
        self.records: List[F4Action] = []
        if self.env_name == Env.connectx:
            return self.run_kagele(state)
        return self.run_self(state)

    def run_kagele(self, state=None):
        from common.util.log import JSON_TMP_FILE

        records = self.env.run(self.players)
        JSON_TMP_FILE.write_file(records)
        for d in records[1:]:
            self.records.append(
                F4Action().laod_from_karord(
                    board=d[0]["observation"]["board"],
                    action=d[0]["action"] + d[1]["action"],
                )
            )

        step = records[-1][0]["observation"]["step"]
        return -1 if records[-1][0]["reward"] == 0 else (step + 1) % 2

    def render(self, mode=None, **kw):
        if self.env_name == Env.connectx and mode == "html":
            ret = self.env.render(mode=mode, **kw)
            File(f"{DATA_PATH}/{self.env_name}.html").write_file(ret)
        cur = self.state.dst
        for r in self.records:

            logger.info(f"doaction: {r}")
            act = cur.get_action(r.action)
            if not act:
                logger.info("gg")
                break
            cur = act.dst
            # f2 = F4State(C.grid_to_mask(r.board)).init_root(C.HEIGHT, C.WIDTH)
            # if f2.mask != cur.mask:
            #     logger.info(f"gbg\n{bin(cur.mask)}\n{bin(f2.mask)}\n" + f2.to_str())
            # logger.info(cur.to_str())

    def play(self, player: Algo):
        action = player.search(self.init_state)
        return action.dst.best_action
