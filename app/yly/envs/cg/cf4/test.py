from common.util.export import TestBase, logger, Module
from common.algo.export import random_seed, ALgoManage
from common.third_service.export import CodingGame


from .model.cf4state import F4State, F4Action
from .cg import CgMuiltCf4
from .model.constant import C
from .util import Pm
from typing import List


class C4Test(TestBase):
    def prepare(self, args=None):
        self.c = CodingGame(CgMuiltCf4.name)

    def cg_play(self):
        Module().compile_one(CgMuiltCf4.main_py())
        CodingGame("cf4").pk(
            Module.RUN_TMP_PATH, CgMuiltCf4.game_id, CgMuiltCf4.agentsIds
        )
        self.cg_replay()

    def cg_replay(self):
        ALgoManage(CgMuiltCf4.name).set_state(F4State.new_state()).actor([Pm.ab1])

    def test_dev2(self):
        s = F4State.new_state()
        # logger.info(s)
        a = s.get_action(0).dst.get_action(0)
        logger.info(a.dst)

    def test_dev3(self):
        s = F4State.new_state(17740539234841)
        logger.info(s)

    def test_debug(self):
        pass


if __name__ == "__main__":
    random_seed()
    C4Test().run()
