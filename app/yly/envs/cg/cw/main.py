from .cg import CgCw, World
from .model.state import CwState, ENV
from .model.constant import CASES, C
from .shape.b_line_help import BlineHelp, BM
from common.util.export import ToolBase, logger, Module
from common.third_service.export import CodingGame, uu
from common.algo.export import ALgoManage


class TestCw(ToolBase):
    def prepare(self):
        self.al = ALgoManage()
        ENV.load(CASES.MAP1)
        self.s = CwState(CASES.S1_1)

    def dev(self):
        logger.debug(self.s.show())

    def fight(self):
        self.al.set_players([self.al.ab(1), self.al.ab(1)]).fight()


if __name__ == "__main__":
    TestCw().run()
