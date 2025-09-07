from common.algo.search.algo import Algo
from common.algo.search.state import State, Action
from common.algo.search.alphabate_search import AbDev
from common.util.export import (
    logger,
    File,
    List,
    defaultdict,
    Dict,
    ThreadManage,
    progress_bar,
)
from common.third_util.export import PtTable, TableModel
import time


class PM:
    @staticmethod
    def ab(n):
        return AbDev(f"ab{n}").load(n)

    @staticmethod
    def am(n):
        return AbDev(f"am{n}").load(n, search_type=AbDev.AB_MUCH)

    @staticmethod
    def ad(n):
        return AbDev(f"ad{n}").load(n, search_type=AbDev.AB_TYPE)

    def ab5():
        return [PM.ab(i + 1) for i in range(5)]

    def am5():
        return [PM.am(i + 1) for i in range(5)]

    def ad5():
        return [PM.ad(i + 1) for i in range(5)]


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
        return [
            "key",
            "rate",
            "WIN",
            "DRAW",
            "MAX_TIME",
            "ALL_TIME",
            "SCORE",
        ]

    @property
    def rate(self):
        return (self.WIN + self.DRAW * 0.5) / self.all_count

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
        return [v.rate, v.WIN, v.DRAW, -v.MAX_TIME, -v.ALL_TIME, v.SCORE]


class FIGHT_TYPE:
    SIGNAL = "SIGNAL"
    DTURN = "DTURN"
    MUCH_THREAD = "MUCH_THREAD"


class ALgoManage:
    record_dir = ""
    file_path = None
    record_model = AlgoInfo

    def set_players(self, players: List[Algo]):
        self.players: List[Algo] = players
        self.record_model.clear()
        self.a_r: Dict[str, AlgoInfo] = {
            p.get_name(): AlgoInfo(p.get_name()) for p in players
        }
        return self

    def set_state(self, state):
        self.state: State = state
        return self

    def get_state(self, idx, dst=None) -> State:
        if callable(self.state):
            return self.state(idx, dst)
        return dst

    def get_players_turn_simple(self, pk_round, tp):
        ret = []
        for _ in range(pk_round):
            for i in range(len(self.players)):
                for j in range(i + 1, len(self.players)):
                    if tp == FIGHT_TYPE.SIGNAL:
                        ret.append([self.players[i], self.players[j]])
                    else:
                        ret.append([self.players[i], self.players[j]])
                        ret.append([self.players[j], self.players[i]])
        return ret

    def fight(self, pk_round=1, tp=None, run_type=None):
        players = self.get_players_turn_simple(pk_round, tp)
        if run_type == FIGHT_TYPE.MUCH_THREAD:
            ThreadManage().run(self.pk, players)
        else:
            for i, p in enumerate(players):
                self.pk(p)
                progress_bar(i + 1, len(players))
        return self

    def show(self):
        return str(PtTable().load_form_model(self.record_model))

    def pk(self, players1: List[Algo]):
        win_idx, turn_idx = self.actor(players1)
        s = f"{players1[0].get_name()} pk {players1[1].get_name()} "
        for i, p in enumerate(players1):
            key = p.get_name()
            if win_idx == -1:
                self.a_r[key].update_result("DRAW")
                s += f"[{key}][DRAW]"
            elif win_idx == i:
                self.a_r[key].update_result("WIN")
                s += f"[{key}][WIN]"
            else:
                self.a_r[key].update_result("LOSE")
        logger.debug(f"{s}[{win_idx}] turn:{turn_idx} file_path:{self.file_path}")
        return win_idx

    max_turn = 250

    def actor(self, players: List[Algo], num=-1):
        """
        返还赢的玩家ID
        """

        player_idx = 0
        self.turn_idx = 0
        s = self.get_state(0, self.state).reset_env()
        for p in players:
            p.reset()
        self.rewards = [[0] * len(players)]
        while num != 0:
            num -= 1
            if s.get_done():
                self.record(players, None, player_idx, s)
                break
            b = time.time()
            p = players[player_idx]
            p.state_num = 0
            a = p.search(s)
            if a is None:
                self.record(players, a, player_idx, s)
                return (
                    s.get_win_player(self.rewards, (player_idx + 1) % len(players)),
                    self.turn_idx,
                )
            self.a_r[p.get_name()].update(
                int((time.time() - b) * 1000), p.state_num, a.get_reward()
            )
            self.record(players, a, player_idx, s)
            player_idx = (player_idx + 1) % len(players)
            self.turn_idx += 1
            if self.turn_idx >= self.max_turn:
                break
            s = self.get_state(self.turn_idx, s.do_action(a))
        # if s:
        #     self.record(players, s)
        return s.get_win_player(self.rewards, player_idx), self.turn_idx

    def set_record_dir(self, path: str):
        self.record_dir = path
        return self

    def record(self, players: List[Algo], a: Action, player_idx, s: State):
        if not self.record_dir:
            return
        self.rewards.append(self.rewards[-1].copy())
        reward = 0

        action_s = ""
        if a is not None:
            reward = a.get_reward()
            action_s = a.show()
        msgs = [
            s.show(),
            f"turn: {self.turn_idx}; reward_all: {self.rewards[-1]};",
            f"{players[player_idx].get_name()} do {action_s}",
            "",
        ]
        self.rewards[-1][player_idx] += reward

        file_name = "_pk_".join([v.get_name() for v in players])
        self.file_path = f"{self.record_dir}/pk/{file_name}.log"
        fp = File(self.file_path).get_writer()
        fp.write("\n".join(msgs))
        fp.flush()

    def train(self, players: List[Algo]):
        pass
