from common.util.export import TestBase, logger, Module
from common.third_util.export import CodingGame
from app.yly.game.envs.cw.cg import CgCw


class CwTest(TestBase):
    def test_pk(self):
        Module().compile_one(CgCw)
        CodingGame(CgCw.name).pk(Module.RUN_TMP_PATH, CgCw.game_id, CgCw.agentsIds)


if __name__ == "__main__":
    CwTest().run()
