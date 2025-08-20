from common.util.export import TestBase, logger, Module, ii
from common.third_util.export import CodingGame
from common.algo.export import AlphaBateSearch, ALgoManage, Algo
from app.yly.envs.cg.oa.export import CgOa, Rooms, C, PM


class OaTest(TestBase):
    def prepare(self, args=None):
        self.cg = CodingGame(CgOa.name)

    def cg_play(self):
        Module().compile_one("app/yly/game/envs/oa/cg.py")
        self.cg.pk(Module.RUN_TMP_PATH, CgOa.game_id, CgOa.agentsIds)

    # def test_base(self):
    #     """ """
    #     r = Rooms.new(C.INIT_MASK).get_action(2).dst

    #     # a = AlphaBateSearch().search(r)
    #     logger.info(r)

    def run_algo_case(self, algo: Algo):
        for a, v in C.get_cases().items():
            s = Rooms.new(a)
            a = algo.search(s)
            self.expect(str(a), v, s)

    def test_dev1(self):
        s2 = ii("1 8 7 6 6 4 4 4 4 4 0 0")
        s = Rooms.new_room(0, s2)
        self.expect(s.boards, s2, s)

    def test_dev2(self):
        s = Rooms.new(78401807947313188929)
        a = s.get_action(5)
        self.expect(a.reward, 9, f"{s}\n{a}\n{a.dst}")

    def fight(self):
        ALgoManage(CgOa.name).set_players([PM.ab1, PM.ab2, PM.ab3, PM.ab4]).set_state(
            Rooms.new(C.INIT_MASK)
        ).fight()

    def pk(self):
        players = [PM.ab1, PM.ab2]
        al = (
            ALgoManage()
            .set_state(Rooms.new(C.INIT_MASK))
            .set_record_dir(self.cg.get_local_path("pk"))
        )
        win_idx = al.actor(players, 200)
        logger.map(win_idx=win_idx, log=al.file_path)

    def test_rule(self):
        s = Rooms.new(74939897936884006912)
        self.expect(list(s.get_actions().keys()), [5], s)

    def debug(self):
        self.pk()


if __name__ == "__main__":
    OaTest().run()
