from typing import List
from common.algo.search.algo import Algo
from common.algo.search.state import State, Action
from common.util.export import logger


class ALgoManage:
    def fight(self, players: List[Algo], pk_fun, pk_round=1):
        self.fight_result = {
            v.name: dict(LOSE=0, use_time=0, max_time=0) for v in players
        }
        for _ in range(pk_round):
            for i in range(len(players)):
                self.pk(pk_fun, [players[i], players[i]])
                for j in range(i + 1, len(players)):
                    self.pk(pk_fun, [players[i], players[j]])
                    self.pk(pk_fun, [players[j], players[i]])
        logger.table(self.fight_result, lambda a: [a["LOSE"]])
        return self.fight_result

    def pk(self, pk_fun, players1: List[Algo]):
        win_idx: int = self.actor(players1, pk_fun, with_log=False)
        s = f"{players1[0].get_name()} pk {players1[1].get_name()} "
        if 0 <= win_idx < len(players1):
            self.fight_result[players1[win_idx].get_name()]["LOSE"] += 1
            s += f"[{players1[win_idx].get_name()}][LOSE]"
            logger.info(s)
        return self

    def actor(self, players: List[Algo], s: State, max_turn=-1, with_log=True):
        """
        返还输的玩家ID
        """
        player_idx = 0
        while not s.done and max_turn != 0:
            if with_log:
                logger.info(f"turn: {max_turn} \n{s}")
            a = players[player_idx].search(s)
            player_idx = (player_idx + 1) % len(players)
            if a is None:
                return player_idx if s.get_win_player() else -1
            if with_log:
                logger.info(a)
            max_turn -= 1
            s = a.dst
            s.get_actions()
        if s and with_log:
            logger.info(s)
        return player_idx if s.get_win_player() else -1
