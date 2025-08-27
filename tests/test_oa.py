from common.util.export import TestBase, logger, Module, ii
from common.third_util.export import CodingGame
from common.algo.export import AlphaBateSearch, ALgoManage, Algo
from app.yly.envs.cg.oa.export import CgOa, Rooms, C, PM


class OaTest(TestBase):
    def prepare(self, args=None):
        self.cg = CodingGame(CgOa.name)
        self.al = (
            ALgoManage()
            .set_state(Rooms.new(C.INIT_MASK))
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

    def test_dev2(self):
        s = Rooms.new(78401807947313188929)
        a = s.get_action(5)
        self.expect(a.reward, 9, f"{s}\n{a}\n{a.dst}")

    def test_ab(self):
        s = Rooms.new(4724692046856857583875)
        a1 = PM.ab1.search(s)
        self.expect(a1.get_reward(), 5, s)
        a3 = PM.ab1.search(a1.dst)
        self.expect(a3.get_reward(), 0, a1.dst)
        a2 = PM.ab2.search(s)
        self.expect(a2.get_reward(), 5, s)

    def fight(self, players, tp=None):
        self.al.set_players(players).fight(tp=tp)

    def fight_all(self):
        self.fight(PM.all())

    def pk(self):
        self.fight([PM.ab5, PM.bl1], ALgoManage.SIGNAL)

    def test_rule(self):
        s = Rooms.new(74939897936884006912)
        self.expect(list(s.get_actions().keys()), [5], s)
        s = Rooms.new(2342206402455670848)
        self.expect(list(s.get_actions().keys()), [1, 2, 3, 4], s)

    def debug(self):
        self.pk()


if __name__ == "__main__":
    OaTest().run()
