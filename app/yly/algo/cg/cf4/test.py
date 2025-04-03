from common.algo.test import TestBase
from app.yly.algo.cg.cf4.main import logger, F4State, Env, PLAYERS, S


class C4Test(TestBase):
    def __init__(self):
        super().__init__()

    def test_pk(self):
        players = ["kd1", "ab1"]
        env = Env(Env.connectx, debug=1)
        # Play as the first agent against "negamax" agent.
        result = env.run(players)
        env.render(mode="html", width=500, height=450)
        if result > 0:
            logger.info(f"[{players[result]}][{S[result]}] win")
        else:
            logger.info("no win")

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
        s = []
        for win_num, op_num, draw_num, key in result:
            pk_all = win_num + op_num + draw_num
            s.append(
                f"{key}-> win_num:{win_num}; op_num:{op_num}; draw_num:{draw_num} win_rata:{'%.2f'}"
            )


if __name__ == "__main__":
    C4Test().run()
