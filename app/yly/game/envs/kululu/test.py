from common.util.export import TestBase, logger, Module
from common.algo.export import ALgoManage
from common.third_util.export import CodingGame
from app.yly.game.envs.kululu.cg import Kululu
from app.yly.game.envs.kululu.util import Pm
from .model.grid import Grid


class KululuTest(TestBase):
    def prepare(self, args=None):
        self.c = CodingGame(Kululu.name)

    def cg_play(self):
        Module().compile_one(Kululu.main_py())
        self.c.pk(Module.RUN_TMP_PATH, Kululu.game_id, Kululu.agentsIds)
        self.cg_replay()

    def cg_replay(self):
        frames = self.c.get_cg_frames_stderror()

        def util(idx: int, dst):
            return Grid().load_from_json(**frames[idx].stderr)

        ALgoManage(Kululu.name).set_state(util).actor([Pm.ab1], len(frames))

    def debug(self):
        self.cg_play()


if __name__ == "__main__":
    KululuTest().run()
