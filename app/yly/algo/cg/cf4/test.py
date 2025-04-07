from common.util.test import TestBase, logger
from app.yly.algo.cg.cf4.main import F4State, Env, PLAYERS, S


class C4Test(TestBase):
    def __init__(self):
        super().__init__()

    def test_pk(self):
        players = ["ab1", "ab3"]
        env = Env(Env.connectx, debug=1)
        # Play as the first agent against "negamax" agent.
        result = env.run(players)
        env.render(mode="html", width=500, height=450)
        if result > 0:
            logger.info(f"[{players[result]}][{S[result]}] win")
        else:
            logger.info("no win")

    def test_full(self):
        e = Env(4432800661633, width=7, height=6)
        self.expect(e.state.get_action(3), None, e.state.to_str())

    def test_2(self):
        e = Env(4432997729025, width=7, height=6)
        self.expect(e.play("ab1"), 0, e.state.to_str())

    def test_fight(self):
        """
        所有玩家一起战斗
        看看谁是第一名
        """

        keys = list(PLAYERS.keys())
        fight_result = {v: [0, 0, 0, v] for v in keys}

        def update(state, players):
            if state is None:
                raise Exception(players)
            if state == -1:
                fight_result[players[0]][1] += 1
                fight_result[players[1]][1] += 1
            else:
                fight_result[state][0] += 1
                fight_result[1 - state][2] += 1

        for pk_num in range(2):
            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    ps = [keys[i], keys[j]]
                    update(Env().run(ps), ps)
                    ps.reverse()
                    update(Env().run(ps), ps)
        result = sorted(fight_result.values(), reverse=True)
        logger.table(result)


if __name__ == "__main__":
    C4Test().run()
