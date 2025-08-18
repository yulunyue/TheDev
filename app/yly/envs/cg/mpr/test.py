from common.util.export import TestBase, logger, File, Module, ThreadManage

from app.yly.envs.cg.mpr.cg import Mpr
from app.yly.envs.cg.mpr.util import Util


class MprTest(TestBase):
    def prepare(self):
        self.c = Util(Mpr.name)

    def cg_play(self):
        Module().compile_one(Mpr.main_py())
        File(Module.RUN_TMP_PATH)
        self.c.pk(Module.RUN_TMP_PATH, Mpr.game_id, Mpr.agents_ids)

    def show(self):
        self.c.show()

    def debug(self):
        pass


if __name__ == "__main__":
    MprTest().run()
