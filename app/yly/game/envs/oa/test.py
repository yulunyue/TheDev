from common.util.export import TestBase, logger, Module, ii
from common.third_util.export import CodingGame
from common.algo.export import AlphaBateSearch, ALgoManage, Algo
from app.yly.game.envs.oa.cg import CgOa, Rooms, C, PM


class CwTest(TestBase):
    def test_cg(self):
        Module().compile_one("app/yly/game/envs/oa/cg.py")
        CodingGame(CgOa.name).pk(Module.RUN_TMP_PATH, CgOa.game_id, CgOa.agentsIds)

    def test_base(self):
        r = Rooms.new(C.INIT_MASK).get_action(2).dst

        # a = AlphaBateSearch().search(r)
        logger.info(r)

    def test_case(self, algo: Algo):
        for a, v in C.get_cases().items():
            s = Rooms.new(a)
            a = algo.search(s)
            self.expect(str(a), v, s)

    def test_dev(self):
        self.test_case(PM.ab1)

    def test_dev1(self):
        s2 = ii("1 8 7 6 6 4 4 4 4 4 0 0")
        s = Rooms.new_room(0, s2)
        self.expect(s.boards, s2, s)

    def test_debug(self):
        self.test_fight()

    def test_fight(self):
        ALgoManage(CgOa.name).set_players(
            [PM.ab1, PM.ab2, PM.ab3, PM.ab4]
        ).set_init_state(Rooms.new(C.INIT_MASK)).fight()

    def test_rule(self):
        s = Rooms.new(74939897936884006912)
        self.expect(list(s.get_actions().keys()), [5], s)


if __name__ == "__main__":
    CwTest().run()
