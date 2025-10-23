from common.util.export import ToolBase, logger, Module, List
from common.algo.export import random_seed, ALgoManage, Algo
from common.third_service.export import CodingGame, uu
from app.yly.envs.cg.cf4.export import (
    F4StateDev as F4State,
    CgMuiltCf4,
    C,
    CASES,
    Kagle,
)


class ToolCf4(ToolBase):

    def prepare(self, args=None):
        C.load(1)
        self.c = CodingGame(CgMuiltCf4.name)
        self.init_state = F4State.new(C.INIT_MASK)
        self.al = (
            ALgoManage().set_state(self.init_state).set_record_dir(uu(CgMuiltCf4.name))
        )

    def test_am1(self):
        self.run_algo(self.al.am(1))

    def cg_play(self):
        Module().compile_one(CgMuiltCf4.main_py())
        CodingGame(CgMuiltCf4.name).pk(
            Module.RUN_TMP_PATH, CgMuiltCf4.game_id, CgMuiltCf4.agentsIds
        )
        self.cg_replay()

    def cg_submit(self):
        Module().compile_one(CgMuiltCf4.main_py())
        CodingGame(CgMuiltCf4.name).submit(
            Module.RUN_TMP_PATH,
            CgMuiltCf4.game_id,
        )

    def cg_replay(self):
        self.c.replay(self.init_state, self.al.am(1))

    def f1(self):
        self.al.set_players([self.al.mc()], [self.al.mc()]).fight()

    def f2(self):
        self.al.set_players(self.al.ams(4), self.al.ams(4)).fight()

    def dev(self):
        s = F4State.new(0x301012B2A01010102)
        logger.debug(s.show())
        for i in range(1, 2):
            a = self.al.ab(i).search(s)
            logger.debug(a.show())
        logger.debug(s.dump_tree(1))

    def train(self):
        self.al.train([self.al.mc(100)])

    def debug(self):
        self.dev()


if __name__ == "__main__":
    random_seed(3)
    ToolCf4().run()
