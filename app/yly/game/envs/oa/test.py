from common.util.export import TestBase, logger, Module
from common.third_util.export import CodingGame
from app.yly.algo.cg.cw.main import CgCw


class CwTest(TestBase):
    def test_pk(self):
        path = Module().compile_one(CgCw)
        CodingGame("cgcw").pk(path, CgCw.game_id, CgCw.agentsIds)


if __name__ == "__main__":
    CwTest().run()
