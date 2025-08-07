from common.util.export import TestBase, logger, File, Module, ThreadManage
from common.third_util.export import CodingGame
from app.yly.game.envs.mpr.cg import Mpr
from app.yly.game.envs.mpr.util import Util


class MprTest(TestBase):
    def test_cg(self, mode):
        Module().compile_one(Mpr.main_py())
        File(Module.RUN_TMP_PATH).replace({"MOCK_MODE": mode})
        CodingGame(Mpr.name).pk(Module.RUN_TMP_PATH, Mpr.game_id, Mpr.agents_ids)

    def test_show(self, mode):
        Util().show(CodingGame(Mpr.name).get_cg_frames(), mode)

    def test_debug(self):
        pass


if __name__ == "__main__":
    MprTest().run()
