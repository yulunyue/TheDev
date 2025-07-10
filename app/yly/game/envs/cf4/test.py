from common.util.export import TestBase, logger, Module
from common.algo.export import random_seed, ALgoManage
from common.third_util.export import CodingGame


from app.yly.game.envs.cf4.model.cf4state import F4State, F4Action
from app.yly.game.envs.cf4.cg import CgMuiltCf4
from app.yly.game.envs.cf4.model.constant import C
from .util import Pm
from typing import List

GRID_ENV = 0


class C4Test(TestBase):

    def test_cases(self):
        for k, v in C.get_cases().items():
            k = C.any_to_mask(k, GRID_ENV)
            s = F4State.new_state(k)
            a = Pm.ab1.search(s)
            self.expect(a.action, v, s)

    def test_cgplay(self):
        path = Module().compile_one("app/yly/algo/cg/cf4/solution.py")
        CodingGame("cf4").pk(path, CgMuiltCf4.game_id, CgMuiltCf4.agentsIds)

    def test_dev1(self):
        s = F4State.new_state(C.any_to_mask(C.S1, GRID_ENV))
        Pm.bl1.search(s)
        logger.info(s)

    def test_dev2(self):
        s = F4State.new_state(C.init_masks[GRID_ENV])
        # logger.info(s)
        a = s.get_action(0)
        logger.info(a.dst)
        # a = a.dst.get_action(0)
        # logger.info(a.dst)

    def test_dev3(self):
        s = F4State.new_state(17730707194377)
        logger.info(s)

    def test_debug(self):
        self.test_dev2()


if __name__ == "__main__":
    random_seed()
    C4Test().run()
