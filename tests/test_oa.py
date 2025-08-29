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
        self.cg.replay(self.init_state, PM.ab(5))


    def pk2(self):
        self.al.set_players([
            PM.ab(1), PM.ab(3)
        ]).fight(tp=FIGHT_TYPE.SIGNAL)
     

    def pk2(self):
        self.al.set_players(PM.all()).fight()

    def debug(self):
        # s=Rooms.new(852117536177685595136).get_action(4).dst
        # logger.info(s)
        self.cg_replay()


if __name__ == "__main__":
    OaTest().run()
