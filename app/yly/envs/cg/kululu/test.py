from common.util.export import TestBase, logger, Module
from common.algo.export import ALgoManage
from common.third_service.export import CodingGame
from app.yly.envs.cg.kululu.cg import Kululu
from .model.grid import Grid


class KululuTest(TestBase):
    def prepare(self):
        self.c = CodingGame(Kululu.name)

    def play(self):
        Module().compile_one(Kululu.main_py())
        self.c.pk(Module.RUN_TMP_PATH, Kululu.game_id, Kululu.agentsIds)
        self.replay()

    def replay(self):
        frames = self.c.get_cg_frames_stderror()
        g: Grid = Grid().load_from_json(**frames[0].stderr)

        def util(idx: int, dst):
            return g.set_players(frames[idx].stderr["players"])

        ALgoManage().set_record_dir(self.c.get_local_path()).set_state(util).actor(
            [Pm.am1], len(frames)
        )

    def debug(self):
        self.replay()


if __name__ == "__main__":
    KululuTest().run()
