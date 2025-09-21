from common.util.export import TestBase, logger, Module, List
from common.algo.export import random_seed, ALgoManage, Algo
from common.third_service.export import CodingGame, uu
from app.yly.envs.cg.cf4.export import F4StateDev as F4State, CgMuiltCf4, C, CASES


class C4Test(TestBase):
    def run_algo(self, algo: Algo):
        for c, e in CASES.CASES.items():
            s = F4State.new(c)
            a = algo.search(s)
            self.expect(a.action, e, s.show())

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
        CodingGame("cf4").pk(
            Module.RUN_TMP_PATH, CgMuiltCf4.game_id, CgMuiltCf4.agentsIds
        )
        self.cg_replay()

    def cg_replay(self):
        self.c.replay(self.init_state, self.al.am(1))

    def f1(self):
        self.al.set_players([self.al.am(1)], [self.al.am(1)]).fight()

    # def f2(self):
    #     self.al.set_players([PM.am(2), PM.mc(10)]).fight_with_control()

    # def f3(self):
    #     self.al.set_players(PM.ams(5)).fight()

    def run2(self):
        s: F4State = F4State.new(0x154B5CDAA05010101)
        logger.debug(s.show())
        # self.al.am(1).search(s)

        # d = s.get_action(3).get_dst()
        # logger.debug(d.show())
        # logger.debug(s.get_point_scores(3))
        # logger.debug(.get_dst().show())

    def run3(self):
        s = self.init_state.get_action([0, 0, 1]).get_dst()
        self.al.ab(1).search(s)

    def run1(self):
        a = self.al.am(1).search(self.init_state)
        logger.debug(f"{self.init_state.show()}\n{a.show()}\n{a.get_dst().show()}")

    def debug(self):
        self.test_am1()


if __name__ == "__main__":
    random_seed()
    C4Test().run()
