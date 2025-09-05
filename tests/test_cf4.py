from common.util.export import TestBase, logger, Module
from common.algo.export import random_seed, ALgoManage, AbDev
from common.third_service.export import CodingGame
from app.yly.envs.cg.cf4.export import F4State, F4Action, CgMuiltCf4


from typing import List


class C4Test(TestBase):
    def prepare(self, args=None):
        self.c = CodingGame(CgMuiltCf4.name)
        self.ab1 = AbDev("ab1").load(1)
        self.init_satte = F4State.new_state()
        self.al = ALgoManage().set_state(self.init_satte)

    def cg_play(self):
        Module().compile_one(CgMuiltCf4.main_py())
        CodingGame("cf4").pk(
            Module.RUN_TMP_PATH, CgMuiltCf4.game_id, CgMuiltCf4.agentsIds
        )
        self.cg_replay()

    def cg_replay(self):
        ALgoManage(CgMuiltCf4.name).set_state(F4State.new_state()).actor([Pm.ab1])

    def dev(self):
        s = F4State.new_state()
        a = s.get_action(0).dst.get_action(0)
        logger.info(a.dst)

    def dev1(self):
        s = F4State.new_state(17740539234841)
        logger.info(s)

    def dev2(self):
        self.al.set_players([self.ab1, self.ab1]).fight()

    def debug(self):
        pass


if __name__ == "__main__":
    random_seed()
    C4Test().run()
