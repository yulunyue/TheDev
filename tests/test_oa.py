from common.util.export import TestBase, logger, Module, ii
from common.third_service.export import CodingGame, uu, CGFrames
from common.algo.export import AlphaBateSearch, ALgoManage, Algo,FIGHT_TYPE
from app.yly.envs.cg.oa.export import CgOa, Rooms, C, PM


class OaTest(TestBase):
    def prepare(self, args=None):
        self.cg = CodingGame(CgOa.name)
        self.init_state = Rooms.new(C.INIT_MASK)
        self.al = ALgoManage().set_state(self.init_state).set_record_dir(uu(CgOa.name))

    def cg_make(self):
        Module().compile_one(CgOa.main_py())

    def cg_play(self):
        self.cg_make()
        self.cg.pk(Module.RUN_TMP_PATH, CgOa.game_id, CgOa.agentsIds)
        self.cg_replay()

    def cg_replay(self):
        self.state = self.init_state

        def util(a: CGFrames, b: CGFrames):
            if b.stdout != "":
                self.state = self.state.get_action(int(b.stdout)).get_dst()
            return self.state

        self.cg.replay(util, PM.ab(5))

    def run_algo_case(self, algo: Algo):
        for a, v in C.get_cases().items():
            s = Rooms.new(a)
            a = algo.search(s)
            self.expect(str(a), v, s)

    def test_dev1(self):
        s2 = ii("1 8 7 6 6 4 4 4 4 4 0 0")
        s = Rooms.new(C.encode_data(0, s2))
        self.expect(s.boards, s2, s)

    def pk2(self):
        self.al.set_players([
            PM.ab(1), PM.ab(3)
        ]).fight(tp=FIGHT_TYPE.SIGNAL)
     

    def dev(self):
        PM.mc().search(self.init_state)

    def debug(self):
        self.cg_replay()


if __name__ == "__main__":
    OaTest().run()
