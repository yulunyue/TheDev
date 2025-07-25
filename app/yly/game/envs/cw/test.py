from common.util.export import TestBase, logger, Module
from common.third_util.export import CodingGame
from app.yly.game.envs.cw.cg import CgCw
from .util import Util


class CwTest(TestBase):
    def test_pk(self):
        Module().compile_one(CgCw.main_py())
        CodingGame(CgCw.name).pk(Module.RUN_TMP_PATH, CgCw.game_id, CgCw.agentsIds)

    def test_replay(self):
        Util().replay(CodingGame(CgCw.name))

    def test_debug(self):
        self.test_pk()


if __name__ == "__main__":
    CwTest().run()
