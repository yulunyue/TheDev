from common.util.export import TestBase, logger, Module
from common.third_util.export import CodingGame
from app.yly.game.envs.cw.cg import CgCw, World
from .util import Util


class CwTest(TestBase):
    def prepare(self, args=None):
        self.c = CodingGame(CgCw.name)
        Module().compile_one(CgCw.main_py())

    def test_pk(self):
        self.c.pk(Module.RUN_TMP_PATH, CgCw.game_id, CgCw.agentsIds)

    def test_replay(self):
        Util().replay(self.c)

    def test_debug(self):
        self.test_base(15)

    def test_base(self, aim_id=-1):
        g = Util().replay(self.c, aim_id=int(aim_id)).set_player_id(0)
        self.expect(g.get_best_action(), "", g)


if __name__ == "__main__":
    CwTest().run()
