from common.util.export import TestBase, logger, Module
from common.algo.export import random_seed, ALgoManage
from common.third_util.export import CodingGame


from app.yly.game.envs.cf4.model.cf4state import F4State, F4Action
from app.yly.game.envs.cf4.cg_pullzy import CgMuiltCf4
from app.yly.game.envs.cf4.cg_solve import CgSolve
from app.yly.game.envs.cf4.model.constant import C
from .util import Pm
from typing import List

GRID_ENV = 0


class C4Test(TestBase):

    def test_cases(self):
        for k, v in C.get_cases().items():
            a, b = CgSolve().excecute(k)
            self.expect(a, v, b)

    def test_cgplay(self):
        Module().compile_one("app/yly/game/envs/cf4/cg_pullzy.py")
        CodingGame("cf4").pk(
            Module.RUN_TMP_PATH, CgMuiltCf4.game_id, CgMuiltCf4.agentsIds
        )

    def test_solve(self, idx=1):
        Module().compile_one("app/yly/game/envs/cf4/cg_solve.py")
        CodingGame("cf4").solve(Module.RUN_TMP_PATH, CgSolve.game_id, text_idx=int(idx))

    def test_dev1(self):
        s = F4State.new_state(C.any_to_mask(C.S3, GRID_ENV))
        logger.info(s.get_player_actions(0)[3].dst)

    def test_dev2(self):
        s = F4State.new_state(C.init_masks[GRID_ENV])
        # logger.info(s)
        a = s.get_action(0).dst.get_action(0)
        logger.info(a.dst)

    def test_dev3(self):
        s = F4State.new_state(17740539234841)
        logger.info(s)

    def test_dev4(self):
        logger.info(CgSolve().excecute(C.S3))

    def test_debug(self):
        self.test_cases()


if __name__ == "__main__":
    random_seed()
    C4Test().run()
