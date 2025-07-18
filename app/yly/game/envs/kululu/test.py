from common.util.export import TestBase, logger, Module
from common.third_util.export import CodingGame
from app.yly.game.envs.kululu.cg import Kululu


class CwTest(TestBase):
    def test_pk(self):
        Module().compile_one("app/yly/game/envs/kululu/cg.py")
        CodingGame("Kululu").pk(Module.RUN_TMP_PATH, Kululu.game_id, Kululu.agentsIds)


if __name__ == "__main__":
    CwTest().run()
