from common.util.export import TestBase, logger, Module
from common.algo.export import random_seed
from common.third_util.export import CodingGame
from app.yly.algo.cg.cf4.env import Env, PLAYERS, S, get_player, Algo, SE, C
from app.yly.algo.cg.cf4.cf4state import F4State
from app.yly.algo.cg.cf4.solution import Solution
from typing import List


class C4Test(TestBase):
    def __init__(self):
        super().__init__()

    def test_base67(self):
        C.load(6, 7)
        w1, h1 = C.WIDTH - C.inarow + 1, C.HEIGHT - C.inarow + 1
        SIZE = C.WIDTH * C.HEIGHT
        self.expect(
            len(C.lines),
            C.WIDTH * h1 + C.HEIGHT * w1 + 2 * w1 * h1,
        )
        self.expect(
            C.lines[:4],
            [
                [[0, 0, 0, 0], [0, 1, 1, 0], [0, 2, 2, 0], [0, 3, 3, 0]],
                [[0, 0, 0, 1], [1, 0, 1, 1], [2, 0, 2, 1], [3, 0, 3, 1]],
                [[0, 0, 0, 2], [1, 1, 1, 2], [2, 2, 2, 2], [3, 3, 3, 2]],
                [[0, 1, 0, 3], [0, 2, 1, 3], [0, 3, 2, 3], [0, 4, 3, 3]],
            ],
        )
        self.expect(C.point_line_id[0], [[0, 0, 0], [1, 1, 0], [2, 2, 0]])
        self.expect(
            C.point_line_id[7 * 6 // 2],
            [[1, 1, 3], [16, 1, 2], [31, 1, 1], [45, 0, 0], [46, 3, 0]],
        )
        c1_mask = 4432678895770
        c1 = F4State.new_state(c1_mask)
        self.expect(
            C.get_grid_sequence(c1.get_grid()),
            "11114",
            c1.to_str(),
        )

        grid_state = F4State.get_init_state()
        mask_except = 0b1000000100000010000001000000100000010000110
        m2 = 0b1000000100000010000001000000100000010001010
        m3 = 0b1000000100000010000001000000100000010001110
        m1 = C.pust_to_mask(mask_except, 0, 0)
        self.expect(m1, m2, bin(m1))
        m1 = C.pust_to_mask(mask_except, 0, 1)
        self.expect(m1, m3, bin(m1))
        return 0
        state = grid_state.get_action(0).dst.get_action(0).dst

        self.expect(state.get_mask(), mask_except, bin(state.get_mask()))
        state = F4State.new_state(mask_except)
        grids = state.get_grid()
        self.expect(len(grids), SIZE)
        self.expect(grids[-C.WIDTH], 1, grids)
        self.expect(grids[-2 * C.WIDTH], 2, grids)
        self.expect(state.depth, 2, state)

    def test_player_all(self, name="ab1"):
        env = Env()
        action = env.play(get_player(name))

    def test_player(self, player="ab3"):
        a = self.get_env(state=4432687285402).play(get_player(player))
        self.expect(a.src.best_action.action, 3, a.dst)

    def test_pk(self, name1, name2):
        players = [get_player(name1), get_player(name2)]
        env = Env()  # , env_name=Env.connectx)
        # Play as the first agent against "negamax" agent.
        result = env.run(players)
        env.render(mode="html", width=500, height=450)
        if result is None:
            logger.info(f"unknow error")
        elif result >= 0:
            logger.info(f"{players} [{players[result].name}][{S[result]}] win")
        else:
            logger.info("no win")

    def test_cg(self):
        path = Module().compile_one(Solution)
        CodingGame("cf4").pk(path, Solution.game_id, Solution.agentsIds)


if __name__ == "__main__":
    random_seed()
    C4Test().run()
