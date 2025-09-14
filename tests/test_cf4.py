from common.util.export import TestBase, logger, Module, List
from common.algo.export import random_seed, ALgoManage, PM, Algo
from common.third_service.export import CodingGame, uu
from app.yly.envs.cg.cf4.export import F4State, CgMuiltCf4, C, CASES


class C4Test(TestBase):
    def run_algo(self, algo: Algo):
        for k, v in CASES.ALL.items():
            s = F4State.new(k)
            a = algo.search(s)
            self.expect(a.action, v, s.show())

    def prepare(self, args=None):
        C.load(1)
        self.c = CodingGame(CgMuiltCf4.name)
        self.init_state = F4State.new()
        self.al = (
            ALgoManage().set_state(self.init_state).set_record_dir(uu(CgMuiltCf4.name))
        )

    def cg_play(self):
        Module().compile_one(CgMuiltCf4.main_py())
        CodingGame("cf4").pk(
            Module.RUN_TMP_PATH, CgMuiltCf4.game_id, CgMuiltCf4.agentsIds
        )
        self.cg_replay()

    def cg_replay(self):
        self.c.replay(self.init_state, PM.am(4))

    def fight2(self):
        self.al.set_players([PM.am(2), PM.am(5)]).fight()
        logger.debug(self.al.show())

    def fc(self):
        self.al.set_players([PM.am(5), PM.am(2)]).fight_with_control()

    def fight(self):
        self.al.set_players(PM.ams(5)).fight()
        logger.debug(self.al.show())

    def run2(self):
        s = self.init_state
        logger.debug(s.show())
        for i in range(3):
            s = s.get_action(0).get_dst()
            logger.debug(s.show())
            s = s.get_action(1).get_dst()
            logger.debug(s.show())
        s = s.get_action(0).get_dst()
        logger.debug(s.show())

    def run1(self):
        s = F4State.new(CASES.CASE1)
        logger.info(s.show())

    def debug(self):
        self.run1()


if __name__ == "__main__":
    random_seed()
    C4Test().run()
