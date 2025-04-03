from common.algo.test import TestBase
from app.yly.algo.cg.cf4.main import logger, F4State, Env, PLAYERS


class C4Test(TestBase):
    def __init__(self):
        super().__init__()

    def test_ka(self):
        from app.yly.algo.kagle.c4 import cell_swarm

        env = Env("connectx", debug=False)
        # Play as the first agent against "negamax" agent.
        env.run([cell_swarm, cell_swarm])
        env.render(mode="html", width=500, height=450)
        # env.run([cell_swarm, "negamax"])
        # print(env.render(mode="human", width=500, height=450))

    def test_pk(self):
        players = list(PLAYERS)


if __name__ == "__main__":
    C4Test().run()
