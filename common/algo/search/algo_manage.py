from common.algo.search.algo import Algo
from common.algo.search.state import State, Action
from common.util.export import logger, File, List, defaultdict
from common.third_util.export import PtTable, TableModel


class AlgoInfo(TableModel):

    WIN = 0
    LOSE = 0
    DRAW = 0
    SCORE = 0
    STATE_NUM = 0
    AVG_STATE_NUM = 0
    MAX_TIME = 0

    def __new__(cls, key) -> "AlgoInfo":
        return super().__new__(cls, key)


class ALgoManage:
    record_dir = ""
    file_path = None

    def set_players(self, players: List[Algo]):
        self.players: List[Algo] = players
        return self

    def set_state(self, state):
        self.state: State = state
        return self

    def get_state(self, idx, dst=None) -> State:
        if callable(self.state):
            return self.state(idx, dst)
        return dst

    def get_players_turn_much(self, pk_round):
        ret = []
        for _ in range(pk_round):
            for i in range(len(self.players)):
                for j in range(len(self.players)):
                    if i != j:
                        ret.append([self.players[i], self.players[j]])
                    ret.append([self.players[j], self.players[i]])
        return ret

    def get_players_turn_simple(self, pk_round):
        ret = []
        for i in range(len(self.players)):
            for j in range(i + 1, len(self.players)):
                ret.append([self.players[i], self.players[j]])
                ret.append([self.players[j], self.players[i]])
        return ret

    def fight(self, pk_round=1):
        AlgoInfo.clear()

        for players in self.get_players_turn_simple(pk_round):
            self.pk(players)
        logger.info(PtTable().load_form_model(AlgoInfo))

    def pk(self, players1: List[Algo]):
        win_idx: int = self.actor(players1)
        s = f"{players1[0].get_name()} pk {players1[1].get_name()} "
        for i, p in enumerate(players1):
            key = p.get_name()
            AlgoInfo(key).MAX_TIME = max(AlgoInfo(key).MAX_TIME, players1[i].use_time)
            AlgoInfo(key).STATE_NUM = max(
                AlgoInfo(key).STATE_NUM, players1[i].state_num
            )
            AlgoInfo(key).AVG_STATE_NUM += players1[i].state_num
            AlgoInfo(key).SCORE += self.rewards[-1][i]
            if win_idx == -1:
                AlgoInfo(key).C_DRAW += 1
                s += f"[{key}][DRAW]"
            elif win_idx == i:
                AlgoInfo(key).WIN += 1
                s += f"[{key}][WIN]"
            else:
                AlgoInfo(key).LOSE += 1
        logger.info(s)
        return self

    def actor(self, players: List[Algo], max_turn=5000):
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
            a = players[player_idx].search(s)
            if a is None:
                self.record(players, a, player_idx, s)
                return s.get_win_player(self.rewards, (player_idx + 1) % len(players))
            self.record(players, a, player_idx, s)
            player_idx = (player_idx + 1) % len(players)
            self.turn_idx += 1
            if self.turn_idx >= max_turn:
                break
            s = self.get_state(self.turn_idx, a.dst)
        # if s:
        #     self.record(players, s)
        return s.get_win_player(self.rewards, player_idx)

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
