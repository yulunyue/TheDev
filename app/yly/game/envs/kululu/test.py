from common.util.export import TestBase, logger, Module
from common.third_util.export import CodingGame
from app.yly.game.envs.kululu.cg import Kululu
from app.yly.game.envs.kululu.util import Util


class KululuTest(TestBase):
    def test_pk(self):
        Module().compile_one(Kululu.main_py())
        CodingGame(Kululu.name).pk(
            Module.RUN_TMP_PATH, Kululu.game_id, Kululu.agentsIds
        )

    def test_replay(self):
        frames = CodingGame(Kululu.name).get_cg_frames()
        Util().replay(frames)

    def test_debug(self):
        self.test_replay()


if __name__ == "__main__":
    CwTest().run()
