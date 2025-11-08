from .cg import CgCw, World
from .model.state import CwState, CwStateDev
from .model.constant import CASES, C
from .shape.b_line_help import BlineHelp, BM
from common.util.export import ToolBase, logger, Module
from common.third_service.export import CodingGame, uu


from common.algo.export import ALgoManage, Algo, AbDev


class TestCw(ToolBase):
    def prepare(self, args=None):
        self.c = CodingGame(CgCw.name)
        self.ab1 = AbDev(f"ab1").load(1)
        CwStateDev.set_envi(CASES.MAP1)
        self.state = CwStateDev.new(CASES.S1_1)
        self.al = ALgoManage().set_state(self.state).set_record_dir(uu(CgCw.name))
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
        pass

    def run_bl(self):
        BM.test()

    def dev(self):
        self.fight()

    def run_base(self, aim_id=1):
        frame = self.c.get_cg_frames_stderror()[int(aim_id)]
        s = World(frame.stderr["state"], 0)

    def run_cases(self, algo: Algo):
        for k, (not_in, ins) in C.get_cases().items():
            s = World(k, 0)
            a = algo.search(s).action
            self.expect(a not in not_in and a in ins, info=f"{s}\n{a}\n{not_in},{ins}")

    def dev(self):
        logger.debug(self.state.show())

    def fight(self):
        self.al.set_players([self.ab1, self.ab1]).fight()


if __name__ == "__main__":
    TestCw().run()
