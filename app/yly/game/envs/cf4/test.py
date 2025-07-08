from common.util.export import TestBase, logger, Module
from common.algo.export import random_seed, ALgoManage
from common.third_util.export import CodingGame


from app.yly.algo.cg.cf4.cf4state import F4State
from app.yly.algo.cg.cf4.solution import Solution

from typing import List

"""
.......
.......
.......
.......
..222..
..111..
"""


class C4Test(TestBase):
    def __init__(self):
        super().__init__()

    def test_pk(self, name1, name2):
        players = [get_player(name1), get_player(name2)]
        env = Env(6, 7)  # , env_name=Env.connectx)
        # Play as the first agent against "negamax" agent.
        result = env.run(players, mode="log")
        if result == 0:
            logger.info("no win")
        elif result == -1:
            logger.info(f"{name1} pk {name2} [{name1}][{S[0]}] win")
        elif result == 1:
            logger.info(f"{name1} pk {name2} [{name2}][{S[1]}] win")
        else:
            logger.info("unknow state")

    def test_fight(self):
        pass

    def test_cg(self, mode="submit"):
        path = Module().compile_one("app/yly/algo/cg/cf4/solution.py")
        if mode == "submit":
            CodingGame("cf4").pk(path, Solution.game_id, Solution.agentsIds)
        elif mode == "replay":
            Solution().replay()

    def test_player(self, name1):
        C.load(6, 7)
        p = get_player(name1)

        a = p.search(F4State.new_state(4432691478663))
        self.expect(a.action, 3, a)

        a = p.search(F4State.new_state(4432687300737))
        self.expect(
            a.action, 4, f"{a}\n{a.src.dump_best_tree(2)}\n{a.get_best_action()}"
        )

    def test_ab3(self):
        C.load(6, 7)
        p = get_player("ab3")
        a = p.search(F4State.new_state(4432687300737))
        # ds = a.src.dump_best_tree(2)
        self.expect(a.action in [1, 4], info=a)

    def test_kl1(self):
        C.load(6, 7)
        p = get_player("kd1")

    def test_fight(self):
        env = Env(6, 7)
        ALgoManage().fight([get_player(k) for k in PLAYERS], env.run)


if __name__ == "__main__":
    random_seed()
    C4Test().run()
