from common.algo.manage import SolutionBase, View, MOD, inf, File

from common.algo.search.mctssearch import MctsSearchTree, MctsNode
from common.algo.search.algo import Algo, np, RandomAlgo
from common.algo.search.alphabate_search import AlphaBateSearch, AbSearchIter

from collections import defaultdict
from typing import Dict, List
from functools import lru_cache
from app.yly.algo.cg.cf4.constant import C, DATA_PATH, S, logger
from app.yly.algo.cg.cf4.cf4action import F4Action
from app.yly.algo.cg.cf4.cf4state import F4State
from app.yly.algo.cg.cf4.kagle import Kagle, KagleAgent, KaggleEnv


class Ab(AlphaBateSearch):

    def __call__(self, env: KaggleEnv, conf: KaggleEnv):
        state = F4State().load_from_kagele(env, conf)
        return self.search(state).action


PLAYERS = dict(
    ab1=lambda: Ab().load(1),
    ab2=lambda: Ab().load(2),
    ab3=lambda: Ab().load(3),
    ab4=lambda: Ab().load(4),
    ab5=lambda: Ab().load(5),
    ab6=lambda: Ab().load(6),
    k1=lambda: KagleAgent(),
    k2=lambda: Kagle().load(),
    # negamax="negamax",
)


def get_player(k) -> Algo:
    player_cls = PLAYERS[k]
    if isinstance(player_cls, str):
        return player_cls
    return player_cls().set_name(k).reset()


class Env:
    connectx = "connectx"

    def __init__(self, height, width, env_name=None, debug=0, state=None, **kw):
        self.env_name = env_name
        self.debug = debug
        self.width = width
        self.height = height
        self.init_state = state
        if env_name == Env.connectx:
            from kaggle_environments import make

            self.env = make(env_name, debug=debug, **kw)
            self.height = self.env.configuration.rows
            self.width = self.env.configuration.columns
            self.env.reset()
        else:
            self.env = None
        C.load(h=self.height, w=self.width)

    def run_self(self, state=None, max_round=256, mode=None):
        player_id = 0
        while max_round and state.done is None:
            action: F4Action = self.players[player_id].search(state)
            self.records.append(action)
            state = action.dst
            player_id = (player_id + 1) % len(self.players)
            max_round -= 1
        if mode:
            self.render(mode)
        return state.done

    def run(self, players: List[Algo], state=None, mode=None):
        if state is None:
            state = F4State.get_init_state()
        self.players = [p.reset() if hasattr(p, "reset") else p for p in players]
        self.records: List[F4Action] = []
        if self.env_name == Env.connectx:
            return self.run_kagele(state)
        return self.run_self(state, mode=mode)

    def run_kagele(self, state=None):
        from common.util.log import JSON_TMP_FILE

        records = self.env.run(self.players)
        JSON_TMP_FILE.write_file(records)
        for d in records[1:]:
            self.records.append(
                F4Action(x=d[0]["action"] + d[1]["action"]).load_from_state(
                    d[0]["observation"]["board"]
                )
            )

        step = records[-1][0]["observation"]["step"]
        return -1 if records[-1][0]["reward"] == 0 else (step + 1) % 2

    def render(self, mode=None, **kw):
        if self.env_name == Env.connectx and mode == "html":
            ret = self.env.render(mode=mode, **kw)
            File(f"{DATA_PATH}/{self.env_name}.html").write_file(ret)
        fp = File(
            f"{DATA_PATH}/pk/{self.players[0].name}[vs]{self.players[1].name}.log"
        )
        datas = []
        for r in self.records:
            datas.append(str(r))
        fp.write_file("\n".join(datas))

    def play(self, player: Algo):
        action = player.search(self.init_state)
        return action
