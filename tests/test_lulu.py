from common.util.export import TestBase, logger, Module
from common.algo.export import ALgoManage, PM
from common.third_service.export import CodingGame, uu
from app.yly.envs.cg.kululu.export import Kululu, Grid, KuState, C


class KululuTest(TestBase):
    def prepare(self):
        self.c = CodingGame(Kululu.name)
        self.al = ALgoManage().set_record_dir(uu(Kululu.name))

    def play(self):
        Module().compile_one(Kululu.main_py())
        self.c.pk(Module.RUN_TMP_PATH, Kululu.game_id, Kululu.agentsIds)
        self.replay()

    def replay(self):
        frames = self.c.get_cg_frames_stderror()
        inps = frames[0].stderr["inputs"]
        h = int(inps[1])
        KuState.set_env(inps[2 : 2 + h], inps[2 + h])
        frames[0].stderr["inputs"] = inps[2 + h :]

        def util(idx: int, dst):
            return KuState(frames[idx].stderr["inputs"])

        self.al.set_state(util).actor([PM.ab(1)], len(frames))

    def dev(self):
        logger.debug(self.state.show())

    def debug(self):
        self.replay()


if __name__ == "__main__":
    KululuTest().run()
