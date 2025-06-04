from typing import List
from common.algo.search.algo import Algo
from common.util.export import logger


class ALgoManage:
    def fight(self, players: List[Algo], pk_fun, pk_round=1):
        self.fight_result = {
            v.name: dict(win=0, draw=0, lose=0, use_time=0, max_time=0) for v in players
        }
        for _ in range(pk_round):
            for i in range(len(players)):
                for j in range(i + 1, len(players)):
                    self.pk(pk_fun, players[i], players[j])
                    self.pk(pk_fun, players[j], players[i])
        logger.table(self.fight_result, lambda a: [a["win"], a["draw"], a["lose"]])
        return self.fight_result

    def pk(self, pk_fun, player1: Algo, player2: Algo):
        result = pk_fun([player1, player2])
        s = f"{player1.get_name()} pk {player2.get_name()} "
        if result == 0:
            self.fight_result[player1.get_name()]["draw"] += 1
            self.fight_result[player2.get_name()]["draw"] += 1
            s += f"[{player1.get_name()}][DRAW][{player2.get_name()}][DRAW]"
        elif result == -1:
            self.fight_result[player1.get_name()]["win"] += 1
            self.fight_result[player2.get_name()]["lose"] += 1
            s += f"[{player1.get_name()}][WIN][{player2.get_name()}][LOSE]"
        elif result == 1:
            self.fight_result[player2.get_name()]["win"] += 1
            self.fight_result[player1.get_name()]["lose"] += 1
            s += f"[{player1.get_name()}][LOSE][{player2.get_name()}][WIN]"
        else:
            raise Exception(player1, player2)
        logger.info(s)
        return self
