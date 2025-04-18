from common.util.test import TestBase, logger
from app.yly.algo.cg.cf4.env import Env, PLAYERS, S, get_player, Algo, SE
from common.algo.search.algo import random_seed
from typing import List


class C4Test(TestBase):
    def __init__(self):
        super().__init__()

    def get_env(self, debug=1, init_state=None):
        return Env(
            debug=debug, width=7, height=6, env_name=None, init_state=init_state
        )  # Env.connectx)

    def get_action(self, init_state=None):
        return self.get_env(init_state=init_state).state

    def test_env(self):
        env = self.get_env()
        a = env.play("kd1")
        self.expect(0, 1, a)

    def test_action(self):
        a = self.get_action().dst.get_action(0)
        a = a.dst.get_action(0)
        self.expect(a.get_points(), [0, 0, 0, 0, 0, 1], a)

    def test_pk(self):
        players = [get_player("kd2"), get_player("kd1")]
        for _ in range(2):
            env = self.get_env()  # , env_name=Env.connectx)
            # Play as the first agent against "negamax" agent.
            result = env.run(players)
            env.render(mode="html", width=500, height=450)
            if result is None:
                logger.info(f"unknow error")
            elif result >= 0:
                logger.info(f"[{players[result].name}][{S[result]}] win")
            else:
                logger.info("no win")
            players.reverse()

    def test_fight(self):
        """
        所有玩家一起战斗看看谁是第一名
        """

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


if __name__ == "__main__":
    random_seed()
    C4Test().run()
