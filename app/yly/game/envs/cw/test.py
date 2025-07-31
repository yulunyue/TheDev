from common.util.export import TestBase, logger, Module
from common.third_util.export import CodingGame
from app.yly.game.envs.cw.cg import CgCw, World
from .util import Util
from common.algo.export import ALgoManage


class CwTest(TestBase):
    def prepare(self, args=None):
        self.c = CodingGame(CgCw.name)
        Module().compile_one(CgCw.main_py())

    def test_pk(self):
        CodingGame(CgCw.name).pk(Module.RUN_TMP_PATH, CgCw.game_id, CgCw.agentsIds)

    def test_replay(self):
        frames = self.c.get_cg_frames_stderror()
        state = World(frames[0].stderr["state"], 0)
        ALgoManage(CgCw.name).set_state(
            state,
            lambda _, i: state.set_shapes(frames[i].stderr["state"].split("|").pop()),
        ).actor([Util.ab1], len(frames))

    def test_debug(self):
        self.test_replay()

    def test_base(self, aim_id=-1):
        frames = self.c.get_cg_frames_stderror()
        state = World(frames[0].stderr["state"], 0)
        max_score, action = g.get_action()
        self.expect(action, max_score)


if __name__ == "__main__":
    CwTest().run()
