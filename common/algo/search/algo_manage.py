from typing import List


class ALgoManage:
    def test_fight(self):

        players = [get_player(k) for k in PLAYERS]
        fight_result = {
            v.name: dict(win=0, draw=0, lose=0, use_time=0, max_time=0) for v in players
        }

        def update(state: int, players: List[Algo]):
            if state is None:
                logger.info(f"unknow state {state} {players[0].name} {players[1].name}")
                return
            if state == -1:
                fight_result[players[0].name]["draw"] += 1
                fight_result[players[1].name]["draw"] += 1
                info = "DRAW"
            else:
                w, l = players[state].name, players[1 - state].name
                fight_result[w]["win"] += 1
                fight_result[l]["lose"] += 1
                info = f"WIN->{w}{S[state]} LOSE->{l}{S[1 - state]} "
            logger.info(f"{players[0].name} pk {players[1].name} {info}")
            for p in players:
                fight_result[p.name]["use_time"] += p.use_time
                fight_result[p.name]["max_time"] = max(
                    fight_result[p.name]["max_time"], p.max_use_time
                )

        for pk_num in range(1):
            for i in range(len(players)):
                for j in range(i + 1, len(players)):
                    ps = [players[i], players[j]]
                    update(self.get_env().run(ps), ps)
                    ps.reverse()
                    update(self.get_env().run(ps), ps)
        logger.table(fight_result, lambda a: [a["win"], a["draw"], a["lose"]])
