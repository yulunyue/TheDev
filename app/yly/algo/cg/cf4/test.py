from common.util.test import TestBase, logger
from app.yly.algo.cg.cf4.env import F4State, Env, PLAYERS, S, get_player, Algo
from typing import List


class C4Test(TestBase):
    def __init__(self):
        super().__init__()

    def test_pk(self):
        players = [get_player("ab1"), get_player("ab3")]
        env = Env(debug=1)
        # Play as the first agent against "negamax" agent.
        result = env.run(players)
        env.render(mode="html", width=500, height=450)
        if result >= 0:
            logger.info(f"[{players[result]}][{S[result]}] win")
        else:
            logger.info("no win")

    def test_full(self):
        e = Env(4432800661633, width=7, height=6)
        self.expect(e.state.get_action(3), None, e.state.to_str())

    def test_2(self):
        e = Env(4432997729025, width=7, height=6)
        self.expect(e.play("ab1"), 0, e.state.to_str())

    def test_table(self):
        logger.table(dict(a=dict(v=3), b=dict(v=2)), key=lambda a: a["v"])

    def test_fight(self):
        """
        所有玩家一起战斗
        看看谁是第一名
        """

        players = [get_player(k) for k in PLAYERS]
        fight_result = {
            v.name: dict(win=0, draw=0, lose=0, name=v, use_time=0, max_time=0)
            for v in players
        }

        def update(state: int, players: List[Algo]):
            if state is None:
                raise Exception(players)
            if state == -1:
                fight_result[players[0].name]["draw"] += 1
                fight_result[players[1].name]["draw"] += 1
                logger.info(f"{players[0].name} draw {players[1]}")
            else:
                fight_result[players[state].name]["win"] += 1
                fight_result[players[1 - state].name]["lose"] += 1
                logger.info(f"{players[state].name} win {players[1 - state].name}")
            for p in players:
                fight_result[p.name]["use_time"] += p.use_time
                fight_result[p.name]["max_time"] = max(
                    fight_result[p.name]["max_time"], p.max_use_time
                )

        for pk_num in range(2):
            for i in range(len(players)):
                for j in range(i + 1, len(players)):
                    ps = [players[i], players[j]]
                    update(Env().run(ps), ps)
                    ps.reverse()
                    update(Env().run(ps), ps)

        logger.table(fight_result, lambda a: [a["win"], a["draw"], a["lose"]])


if __name__ == "__main__":
    C4Test().run()
