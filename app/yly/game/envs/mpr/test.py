from common.util.export import TestBase, logger, Module, ThreadManage
from common.third_util.export import CodingGame
from app.yly.game.envs.mpr.cg import Mpr


class CwTest(TestBase):
    def test_make(self):
        Module().compile_one("app/yly/game/envs/mpr/cg.py")

    def test_pk(self):
        def util(*args):
            CodingGame(Mpr.name).pk(Module.RUN_TMP_PATH, Mpr.game_id, Mpr.agents_ids)

        ThreadManage().run(util, range(4))


if __name__ == "__main__":
    CwTest().run()
