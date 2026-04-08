from common.algo.search.algo import Algo, RandomAlgo, BestAlgo
from common.algo.search.states.state import State, Action
from common.algo.search.alphabate_search import AbDev
from common.algo.search.mctssearch import MctsSearchDev
from common.algo.learn.sarse.qlearning import Qlearning
from common.tool.export import ConfigBase, NumberModel
from common.util.export import (
    logger,
    File,
    List,
    defaultdict,
    Dict,
    ThreadManage,
    os,
    get_dev_log,
)
from common.third_util.pt_table import PtTable
import time


class AlgoInfo(ConfigBase):

    WIN = NumberModel(0)
    LOSE = NumberModel(0)
    DRAW = NumberModel(0)
    SCORE = NumberModel(0)
    MAX_VISTE_NUM = NumberModel(0)
    ALL_VISTE_NUM = NumberModel(0)
    MAX_TIME = NumberModel(0)
    ALL_TIME = NumberModel(0)

    def __init__(self, key):
        self.score = []
        self.all_count = 0
        super().__init__(key)

    @classmethod
    def new(cls, key) -> "AlgoInfo":
        return super().new(key, None)

    @classmethod
    def get_headers(cls):
        return ["key", "WIN", "DRAW", "MAX_TIME", "ALL_TIME", "SCORE", "LOSE"]

    def update(self, tm, state_num, score):
        self.score.append(score)
        self.SCORE += score
        self.ALL_VISTE_NUM += state_num
        self.ALL_TIME += tm
        if state_num > self.MAX_VISTE_NUM.get_value():
            self.MAX_VISTE_NUM.set_value(state_num)
        if tm > self.MAX_TIME.get_value():
            self.MAX_TIME.set_value(tm)

    def update_result(self, tp):
        self.all_count += 1
        f: NumberModel = getattr(self, tp)
        f.set_value(f.get_value() + 1)

    # @classmethod
    # def sort(cls, v: "AlgoInfo"):
    #     return [v.WIN, v.DRAW, -v.MAX_TIME, -v.ALL_TIME, v.SCORE, -v.LOSE]


class ALgoManage:
    record_dir = "data/algo"

    def best(self):
        return BestAlgo("best").load()

    def ad(self, n=10):
        return AbDev(f"ad{n}").load(n, search_type=AbDev.AB_MUCH)

    def dqn(self):
        pass

    def mc(self, n=100):
        return MctsSearchDev(f"mc{n}").load(num_episodes=n)

    def mcs(self, n):
        return [self.mc(i * 10) for i in range(3, n)]

    def ad5(self):
        return [self.ad(i + 1) for i in range(5)]

    def ql(self):
        return Qlearning().load()

    def rd(self):
        return RandomAlgo().load()

    def get_player(self, v):
        if isinstance(v, str):
            if v.startswith("ad"):
                return self.ad(int(v[2:]))
            if v.startswith("mc"):
                return self.mc(int(v[2:]))
            return getattr(self, v)()
        return v

    def set_players(self, players1: List[Algo]):
        self.players: List[List[Algo]] = []
        n = len(players1)
        for i in range(n):
            for j in range(n):
                p1, p2 = players1[i], players1[j]
                if p1.get_name() == p2.get_name():
                    continue
                self.players.append([p1, p2])
        self.set_current_players(self.players[0])
        return self

    def set_current_players(self, players: List[str]):
        self.current_players = [self.get_player(p) for p in players]
        return self

    def set_state(self, state):
        self.state: State = state
        return self

    def fight(self, turn=1):
        idx = 0
        for _ in range(turn):
            for i, p in enumerate(self.players):
                self.pk(p, idx)
                idx += 1
        ret = PtTable().load_form_model(AlgoInfo).show()
        logger.debug(ret)
        return ret

    def pk(self, players1: List[Algo], idx=0):
        self.set_current_players(players)
        p2, turn_idx, s = self.actor(players1, idx)
        s = f"{players1[0].get_name()} pk {players1[1].get_name()} "
        for i, p in enumerate(players1):
            key = p.get_name()
            if p2 is None:
                AlgoInfo.new(players1[0].get_name()).update_result("DRAW")
                AlgoInfo.new(players1[1].get_name()).update_result("DRAW")
                s += f"[{key}][DRAW]"
            elif p2.get_name() == p.get_name():
                AlgoInfo.new(key).update_result("WIN")
                s += f"[{key}][WIN]"
            else:
                AlgoInfo.new(key).update_result("LOSE")
                s += f"[{key}][LOSE]"
        logger.debug(f"{s} turn:{turn_idx}")

    def actor(self, players: List[Algo], idx=0, max_turn=1000):
        """
        返还赢的玩家ID
        """
        self.set_current_players(players)
        self.turn_idx = 0
        self.record_actions: List[Action] = []
        s = self.state
        s.reset_env()
        for i, p in enumerate(players):
            players[i] = self.get_player(p).reset()
        self.log(s.show(), f"actor/{idx}")
        last_a = None
        while self.turn_idx < max_turn:
            if s.game_over():
                break
            p = players[self.turn_idx % len(players)]
            self.turn_idx += 1
            a = p.search(s, last_a=last_a)
            AlgoInfo.new(p.get_name()).update(p.use_time, p.state_num, 0)
            last_a = a
            if a is None:
                return self.actor_return(s)
            self.record_actions.append(a)
            s = s.do_action(a)
            self.record(p, a, f"actor/{idx}")

        return self.actor_return(s)

    def actor_return(self, s: State):
        idx = s.get_win_player()
        if 0 <= idx < len(self.current_players):
            p = self.current_players[idx]
        else:
            p = None
        info = f"\n---turn:{self.turn_idx}---\n{s.show()}\nwin:{p}\n"
        logger.debug(info)
        return p, self.turn_idx, s

    def set_record_dir(self, path: str):
        self.record_dir = path
        return self

    def record(self, p: Algo, a: Action, name):
        msgs = [
            f"turn: {self.turn_idx}; {p.get_name()} do {a.show()}",
            f"{a.get_dst().show()}",
        ]
        self.log("\n".join(msgs), name)

    def log(self, msgs: str, name):
        file_name = "_pk_".join([v.get_name() for v in self.current_players])
        get_dev_log(f"{self.record_dir}/{name}/{file_name}.log").info(msgs)

    def train(self, players: List[Algo], game_batch):
        pass
