from common.util.export import TestBase, logger, Module, ii
from common.third_service.export import CodingGame
from common.algo.export import AlphaBateSearch, ALgoManage, Algo
from app.yly.envs.cg.oa.export import CgOa, Rooms, C, PM


class OaTest(TestBase):
    def prepare(self, args=None):
        self.cg = CodingGame(CgOa.name)
        self.init_state = Rooms.new(C.INIT_MASK)
        self.al = (
            ALgoManage()
            .set_state(self.init_state)
            .set_record_dir(self.cg.get_local_path("pk"))
        )

    def cg_make(self):
        Module().compile_one(CgOa.main_py())

    def cg_play(self):
        self.cg_make()
        self.cg.pk(Module.RUN_TMP_PATH, CgOa.game_id, CgOa.agentsIds)

    def run_algo_case(self, algo: Algo):
        for a, v in C.get_cases().items():
            s = Rooms.new(a)
            a = algo.search(s)
            self.expect(str(a), v, s)

    def test_dev1(self):
        s2 = ii("1 8 7 6 6 4 4 4 4 4 0 0")
        s = Rooms.new(C.encode_data(0, s2))
        self.expect(s.boards, s2, s)

    def fight(self, players, tp=None):
        self.al.set_players(players).fight(tp=tp)

    def fight_all(self):
        self.fight(PM.all())

    def pk1(self):
        self.fight([PM.bl(6), PM.ab(5), PM.ab(5, [0.5])])

    def pk2(self):
        self.fight([PM.ab(5),PM.mc()])
    
    def dev(self):
        PM.mc().search(self.init_state)

    def debug(self):
        self.pk()


if __name__ == "__main__":
    OaTest().run()
