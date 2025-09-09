from common.util.export import TestBase, logger, Module, List
from common.algo.export import random_seed, ALgoManage, AbDev, PM, Algo
from common.third_service.export import CodingGame, uu
from app.yly.envs.cg.cf4.export import F4State, F4Action, CgMuiltCf4, C, CASES


class C4Test(TestBase):
    def run_algo(self, algo: Algo):
        for k, v in CASES.ALL.items():
            s = F4State.new(k)
            a = algo.search(s)
            self.expect(a.action, v, s.show())

    def test_algo(self):
        self.run_algo(PM.am(4))

    def prepare(self, args=None):
        self.c = CodingGame(CgMuiltCf4.name)
        self.init_state = F4State.new(C.init_masks[1])
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

    def dev1(self):
        self.al.set_players([PM.am(1), PM.am(4)]).fight()
        logger.debug(self.al.show())

    def dev2(self):
        self.al.set_players(PM.ad5()).fight()
        logger.debug(self.al.show())

    def dev3(self):
        s = self.init_state.get_action(0).get_dst()
        s = s.get_action(0).get_dst()
        logger.debug(s.show())

    def dev4(self):
        s = F4State.new(CASES.CASE1)
        a = PM.am(4).search(s)
        b = PM.ad(4).search(s)
        logger.map(a=a.action, b=b.action)

    def dev5(self):
        s = F4State.new(CASES.CASE2)
        PM.ad(4).search(s)
        # s.dfs(4)

    def dev6(self):
        s = F4State.new(CASES.CASE3)
        PM.am(4).search(s)

    def debug(self):
        self.dev5()


if __name__ == "__main__":
    random_seed()
    C4Test().run()
