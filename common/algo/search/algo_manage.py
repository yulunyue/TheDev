from common.algo.search.algo import Algo, RandomAlgo
from common.algo.search.state import State, Action
from common.algo.search.alphabate_search import AbDev
from common.algo.search.mctssearch import MctsSearchDev
from common.algo.learn.sarse.qlearning import Qlearning
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
from common.third_util.pt_table import PtTable, TableModel
import time


class AlgoInfo(TableModel):

    WIN = 0
    LOSE = 0
    DRAW = 0
    SCORE = 0
    MAX_VISTE_NUM = 0
    ALL_VISTE_NUM = 0
    MAX_TIME = 0
    ALL_TIME = 0

    def __init__(self, key):
        self.score = []
        self.all_count = 0
        super().__init__(key)

    def __new__(cls, key) -> "AlgoInfo":
        return super().__new__(cls, key)

    @classmethod
    def get_headers(cls):
        return ["key", "WIN", "DRAW", "MAX_TIME", "ALL_TIME", "SCORE", "LOSE"]

    def update(self, tm, state_num, score):
        self.score.append(score)
        self.SCORE += score
        self.ALL_VISTE_NUM += state_num
        self.ALL_TIME += tm
        if state_num > self.MAX_VISTE_NUM:
            self.MAX_VISTE_NUM = state_num
        if tm > self.MAX_TIME:
            self.MAX_TIME = tm

    def update_result(self, tp):
        self.all_count += 1
        setattr(self, tp, getattr(self, tp) + 1)

    @classmethod
    def sort(cls, v: "AlgoInfo"):
        return [v.WIN, v.DRAW, -v.MAX_TIME, -v.ALL_TIME, v.SCORE, -v.LOSE]


class FIGHT_TYPE:
    SIGNAL = "SIGNAL"
    DTURN = "DTURN"


class ALgoManage:
    record_dir = "data/algo"
    file_path = None
    record_model = AlgoInfo

    def ad(self, n=10):
        return AbDev(f"ad{n}").load(n).set_record_dir(self.record_dir)

    def am(self, n=10):
        return (
            AbDev(f"am{n}")
            .load(n, search_type=AbDev.AB_MUCH)
            .set_record_dir(self.record_dir)
        )

    def ab(self, n=10):
        return (
            AbDev(f"ab{n}")
            .load(n, search_type=AbDev.AB_TYPE)
            .set_record_dir(self.record_dir)
        )

    def dqn(self):
        pass

    def mc(self, n=100):
        return MctsSearchDev(f"mc{n}").load(num_episodes=n)

    def mcs(self, n):
        return [self.mc(i * 10) for i in range(3, n)]

    def abs(self, n):
        return [self.ab(i + 1) for i in range(5)]

    def ams(self, v=5):
        return [self.am(i + 1) for i in range(v)]

    def ad5(self):
        return [self.ad(i + 1) for i in range(5)]

    def ql(self):
        return Qlearning().load()

    def rd(self):
        return RandomAlgo().load()

    def set_players(self, players1: List[Algo], players2: List[Algo]):
        self.players: List[List[Algo]] = []
        for p1 in players1:
            for p2 in players2:
                self.players.append([p1, p2])
                self.players.append([p2, p1])
        self.current_player = self.players[0]
        self.record_model.clear()
        self.a_r: Dict[str, AlgoInfo] = {
            p.get_name(): AlgoInfo(p.get_name()) for p in players1 + players2
        }
        return self

    def set_state(self, state):
        self.state: State = state
        return self

    def fight(self):
        for i, p in enumerate(self.players):
            self.pk(p)
        logger.debug(self.show())
        return self

    def fight_with_control(self):
        init_state = s = self.get_state(0, self.state).reset_env()
        history: List[Action] = []
        while True:
            os.system("cls")
            self.view(
                [s.show()]
                + [
                    f"{p.get_name()} do {getattr(p.search(s),'action',None)}"
                    for p in self.current_player
                ]
                + [",".join([str(a.action) for a in history])]
            )
            cmd, *args = input("CMD: ").split(" ")
            if cmd == "r":
                if not args:
                    argsv = 1
                else:
                    argsv = int(args[0])
                history = history[: max(len(history) - argsv, 0)]
                if history:
                    s = history[-1].get_dst()
                else:
                    s = init_state
            elif cmd == "a":
                a = s.get_action(args[0])
                history.append(a)
                s = a.get_dst()
            elif cmd == "p":
                if not args:
                    argsv = 1
                else:
                    argsv = int(args[0])
                for _ in range(argsv):
                    if s.get_done() is not None:
                        break
                    a = self.current_player[len(history) % 2].search(s)
                    history.append(a)
                    s = a.get_dst()
            else:
                break

    def show(self):
        return str(PtTable().load_form_model(self.record_model))

    def pk(self, players1: List[Algo]):
        self.current_player = players1
        win_idx, turn_idx = self.actor(players1)
        s = f"{players1[0].get_name()} pk {players1[1].get_name()} "
        for i, p in enumerate(players1):
            key = p.get_name()
            if win_idx == -1:
                self.a_r[key].update_result("DRAW")
                s += f"[{key}][DRAW]"
            elif win_idx == i:
                self.a_r[key].update_result("WIN")
            else:
                self.a_r[key].update_result("LOSE")
                s += f"[{key}][LOSE]"
        logger.debug(f"{s}[{win_idx}] turn:{turn_idx} file_path:{self.file_path}")
        return win_idx

    def actor(self, players: List[Algo], max_turn=1000):
        """
        返还赢的玩家ID
        """
        self.current_players = players
        self.turn_idx = 0
        s = self.state
        s.reset_env()
        for p in players:
            p.reset()
        self.log(s.show())
        while self.turn_idx < max_turn:
            if s.game_over():
                break
            p = players[self.turn_idx % len(players)]
            self.turn_idx += 1
            # b = time.time()
            p.state_num = 0
            a = p.search(s)
            if a is None:
                return (
                    s.get_win_player(),
                    self.turn_idx,
                )

            self.record(p, a)
            s = s.do_action(a)
        return s.get_win_player(), self.turn_idx

    def set_record_dir(self, path: str):
        self.record_dir = path
        return self

    def record(self, p: Algo, a: Action):
        msgs = [
            f"turn: {self.turn_idx}; {p.get_name()} do {a.show()}",
            f"{a.get_dst().show()}",
        ]
        self.log("\n".join(msgs))

    def log(self, msgs: str, name="pk"):
        file_name = "_pk_".join([v.get_name() for v in self.current_players])
        get_dev_log(f"{self.record_dir}/{name}/{file_name}.log").info(msgs)

    def train(self, players: List[Algo], game_batch):
        pass
