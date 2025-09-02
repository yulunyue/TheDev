from common.util.export import TestBase, logger, Module
from common.third_service.export import CodingGame
from app.yly.envs.cg.cw.cg import CgCw, World, C
from app.yly.envs.cg.cw.model.constant import CASES
from common.algo.export import ALgoManage, Algo
from app.yly.envs.cg.cw.model.b_line_help import BlineHelp, BM


class CwTest(TestBase):
    def prepare(self, args=None):
        self.c = CodingGame(CgCw.name)
        Module().compile_one(CgCw.main_py())

    def get_state(self, i: int, *args):
        frames = self.c.get_cg_frames()
        s = World(frames[i * 2 + 1].stderr["state"], 0)
        s.show_msgs = [
            frames[i * 2].summary,
            frames[i * 2 + 1].summary,
        ]
        return s

    def cg_pk(self):
        CodingGame(CgCw.name).pk(Module.RUN_TMP_PATH, CgCw.game_id, CgCw.agentsIds)
        self.test_replay()

    def cg_replay(self):
        ALgoManage(CgCw.name).set_state(self.get_state).actor(
            [Util.ab1], (len(self.c.get_cg_frames()) // 2 - 1)
        )

    def run_bl(self):
        logger.info(BM.draw(0, 0, 1, 2))
        logger.info(BM.draw(1, 2, 0, 0))
        logger.info(BM.draw(0, 2, 1, 0))
        logger.info(BM.draw(1, 0, 0, 2))

    def debug(self):
        pass

    def run_base(self, aim_id=1):
        frame = self.c.get_cg_frames_stderror()[int(aim_id)]
        s = World(frame.stderr["state"], 0)

    def run_cases(self, algo: Algo):
        for k, (not_in, ins) in C.get_cases().items():
            s = World(k, 0)
            a = algo.search(s).action
            self.expect(a not in not_in and a in ins, info=f"{s}\n{a}\n{not_in},{ins}")

    def dev(self):
        s = World(CASES[5], 0)
        logger.debug(s)


if __name__ == "__main__":
    CwTest().run()
