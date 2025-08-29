from common.algo.search.algo import Algo
from common.algo.search.state import State, Action
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
        super().__init__(key)

    def __new__(cls, key) -> "AlgoInfo":
        return super().__new__(cls, key)

    @classmethod
    def get_headers(cls):
        return [
            "key",
            "WIN",
            "LOSE",
            "MAX_VISTE_NUM",
            "MAX_TIME",
            "ALL_TIME",
            "ALL_VISTE_NUM",
            "DRAW",
            "SCORE",
        ]

    def update(self, tm, state_num, score):
        self.score.append(score)
        self.SCORE += score
        self.ALL_VISTE_NUM += state_num
        self.ALL_TIME += tm
        if state_num > self.MAX_VISTE_NUM:
            self.MAX_VISTE_NUM = state_num
        if tm > self.MAX_TIME:
            self.MAX_TIME = tm

    @classmethod
    def sort(cls, v: "AlgoInfo"):
        return [v.WIN, -v.LOSE, -v.MAX_VISTE_NUM, -v.MAX_TIME]

class FIGHT_TYPE:
    SIGNAL = "SIGNAL"
    DTURN = "DTURN"
    MUCH_THREAD = "MUCH_THREAD"

class ALgoManage:
    record_dir = ""
    file_path = None

    def set_players(self, players: List[Algo]):
        self.players: List[Algo] = players
        AlgoInfo.clear()
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
        logger.info(PtTable().load_form_model(AlgoInfo))

    def pk(self, players1: List[Algo]):
        win_idx, turn_idx = self.actor(players1)
        s = f"{players1[0].get_name()} pk {players1[1].get_name()} "
        for i, p in enumerate(players1):
            key = p.get_name()
            if win_idx == -1:
                self.a_r[key].DRAW += 1
                s += f"[{key}][DRAW]"
            elif win_idx == i:
                self.a_r[key].WIN += 1
                s += f"[{key}][WIN]"
            else:
                self.a_r[key].LOSE += 1
        logger.info(f"{s}[{win_idx}] turn:{turn_idx} file_path:{self.file_path}")
        return self

    max_turn = 250

    def actor(self, players: List[Algo]):
        """
        返还赢的玩家ID
        """

        player_idx = 0
        self.turn_idx = 0
        s = self.get_state(0, self.state).reset_env()
        for p in players:
            p.reset()
        self.rewards = [[0] * len(players)]
        while True:
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
        if a is not None:
            reward = a.get_reward()
        self.rewards[-1][player_idx] += reward
        info = players[player_idx].name
        if reward > 0:
            info += f" CXCWIN {reward}"
        elif reward < 0:
            info += f" CXCLOS {reward}"
        msg = f"{s}\nturn: {self.turn_idx}; reward_all: {self.rewards[-1]}; info: {info}\n"
        file_name = "_pk_".join([v.get_name() for v in players])
        self.file_path = f"{self.record_dir}/{file_name}.log"
        fp = File(self.file_path).get_writer()
        fp.write(msg)
        fp.flush()
