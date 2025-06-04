from common.util.export import TestBase, logger, Module
from common.algo.export import random_seed, ALgoManage
from common.third_util.export import CodingGame

from app.yly.algo.cg.cf4.env import Env, PLAYERS, S, get_player, Algo, SE, C
from app.yly.algo.cg.cf4.cf4state import F4State
from app.yly.algo.cg.cf4.solution import Solution

from typing import List


class C4Test(TestBase):
    def __init__(self):
        super().__init__()

    def test_base67(self, *args):
        C.load(6, 7)
        self.expect(len(C.lines), C.count_line_num(C.inarow))
        self.expect(len(C.point_line_id[0]), 3)
        self.expect(len(C.point_line_id[7 * 6 // 2]), 5)
        c1_mask = 4432678895770
        c1 = F4State.new_state(c1_mask)
        self.expect(
            C.get_grid_sequence(C.get_grid_by_line_state(c1.line_state)),
            "11114",
            c1.to_str(),
        )
        s = F4State.get_init_state()
        self.expect(s.player_id, 0)
        mask_except = 0b1000000100000010000001000000100000010000110
        m2 = 0b1000000100000010000001000000100000010001010
        m3 = 0b1000000100000010000001000000100000010001110
        m1 = C.pust_to_mask(mask_except, 0, 0)
        self.expect(C.mask_to_row(mask_except, 0), 2)
        self.expect(m1, m2, bin(m1))
        m1 = C.pust_to_mask(mask_except, 0, 1)
        self.expect(m1, m3, bin(m1))

        ac = s.get_action(0).dst.get_action(0)
        # self.expect(ac.get_reward(), 1, f"\n{ac.src}\n==>\n{ac.dst}")
        state = ac.dst
        self.expect(state.state, mask_except, bin(state.state))
        # state = F4State.new_state(mask_except)
        grids = C.mask_to_grid(mask_except)
        self.expect(len(grids), C.WIDTH * C.HEIGHT)
        self.expect(grids[-C.WIDTH], 1, grids)
        self.expect(grids[-2 * C.WIDTH], 2, grids)
        self.expect(state.depth, 2, state)

        s = (
            F4State.get_init_state()
            .get_action(2)
            .dst.get_action(2)
            .dst.get_action(3)
            .dst.get_action(3)
            .dst
        )
        self.expect(C.get_point_dr(s.line_state, 5, 4, 0)[0], [0, 0, 2, 0, 1, 1, 2], s)
        self.expect(C.get_point_dr(s.line_state, 5, 4, 1)[0], [0, 0, 0, 2, 1, 1, 2], s)
        s2 = F4State.new_state(4432712451713)
        u1 = C.get_point_dr(s2.line_state, 5, 0, 1)
        self.expect(u1[0], [0, 0, 0, 1, 0, 0, 0], s2)

        s = F4State.get_init_state().get_action(3).dst.get_action(0).dst

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

    def test_cg(self):
        path = Module().compile_one(Solution)
        CodingGame("cf4").pk(path, Solution.game_id, Solution.agentsIds)

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

    def test_fight(self):
        env = Env(6, 7)
        ALgoManage().fight([get_player(k) for k in PLAYERS], env.run)


if __name__ == "__main__":
    random_seed()
    C4Test().run()
