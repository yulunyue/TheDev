from common.algo.search.algo import Algo
from common.algo.search.state import State, Action
from common.util.export import logger, File, List, defaultdict


class ALgoManage:
    def __init__(self, name):
        self.name = name

    def set_players(self, players: List[Algo]):
        self.players: List[Algo] = players
        self.fight_result = defaultdict(
            lambda: dict(WIN=0, LOSE=0, DRAW=0, use_time=0, max_time=0)
        )
        return self

    def set_state(self, state):
        self.state: State = state
        return self

    def get_state(self, idx, dst=None) -> State:
        if callable(self.state):
            return self.state(idx)
        return dst

    def fight(self, pk_round=1):
        for _ in range(pk_round):
            for i in range(len(self.players)):
                for j in range(len(self.players)):
                    if i != j:
                        self.pk([self.players[i], self.players[j]])
                    self.pk([self.players[j], self.players[i]])
        logger.table(self.fight_result, lambda a: [a["WIN"], a["DRAW"], a["DRAW"]])
        return self.fight_result

    def pk(self, players1: List[Algo]):
        win_idx: int = self.actor(players1)
        s = f"{players1[0].get_name()} pk {players1[1].get_name()} "
        keys = [f"{players1[i].get_name()}_{i}" for i in range(len(players1))]
        if 0 <= win_idx < len(players1):
            self.fight_result[keys[win_idx]]["LOSE"] += 1
            self.fight_result[keys[1 - win_idx]]["WIN"] += 1
            s += f"[{keys[win_idx]}][LOSE]"
        else:
            self.fight_result[keys[0]]["DRAW"] += 1
            self.fight_result[keys[1]]["DRAW"] += 1
            s += f"[DRAW]"
        logger.info(s)
        return self

    def actor(self, players: List[Algo], max_turn=200):
        """
        返还输的玩家ID
        """

        player_idx = 0
        self.turn_idx = 0
        s = self.get_state(0)
        self.rewards = [0] * len(players)
        while not s.get_done() and self.turn_idx < max_turn:
            a = players[player_idx].search(s)
            if a is None:
                return s.get_win_player(self.rewards, (player_idx + 1) % len(players))
            self.rewards[player_idx] = a.reward
            self.info(players, s)
            player_idx = (player_idx + 1) % len(players)
            self.turn_idx += 1
            s = self.get_state(self.turn_idx, a.dst)
        if s:
            self.info(players, s)
        return s.get_win_player(self.rewards, player_idx)

    def info(self, players: List[Algo], msg=None):
        msg = f"turn: {self.turn_idx}; reward_all: {self.rewards};{msg}"
        file_name = "_pk_".join([v.get_name() for v in players])
        file_path = f"data/log/algo_pk/{self.name}/{file_name}.log"
        fp = File(file_path).get_writer()
        fp.write(f"{msg}\n")
        fp.flush()
