from common.algo.search.algo import Algo
from common.algo.search.state import State, Action
from common.util.export import logger, File, List, defaultdict


class ALgoManage:
    def set_players(self, players: List[Algo]):
        self.players: List[Algo] = players
        self.fight_result = defaultdict(
            lambda: dict(WIN=0, LOSE=0, DRAW=0, use_time=0, max_time=0)
        )
        return self

    def set_init_state(self, state):
        self.state: State = state
        return self

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

    def actor(self, players: List[Algo], max_turn=-1):
        """
        返还输的玩家ID
        """
        s = self.state
        player_idx = 0
        while not s.get_done() and max_turn != 0:
            a = players[player_idx].search(s)
            self.info(players, f"turn: {max_turn} {s}")
            player_idx = (player_idx + 1) % len(players)
            if a is None:
                return player_idx if s.get_win_player() else -1
            max_turn -= 1
            s = a.dst
        if s:
            self.info(players, f"last_turn: {max_turn} {s}")
        return player_idx if s.get_win_player() else -1

    def info(self, players: List[Algo], msg):
        file_name = "_pk_".join([v.get_name() for v in players])
        file_path = f"data/log/algo_pk/{file_name}.log"
        fp = File(file_path).get_writer()
        fp.write(f"{msg}\n")
        fp.flush()
