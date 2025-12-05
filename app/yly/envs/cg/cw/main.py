from .cg import CgCw, World
from .model.state import CwState, ENV
from .model.constant import CASES, C
from .shape.b_line_help import BlineHelp, BM
from common.util.export import ToolBase,log, logger, Module
from common.third_service.export import CodingGame, uu
from common.algo.export import ALgoManage


class Solution(ToolBase):
    def prepare(self):
        self.al = ALgoManage()
        ENV.load(CASES.MAP1)
        self.s = CwState.new(CASES.S1_1)

    def dev(self):
        log.debug(self.s.show())
        for a in self.s.get_sort_actions():
            log.debug(a.show())
            log.debug(a.get_dst().show())

    def fight(self):
        self.al.set_players([self.al.ab(1), self.al.ab(1)]).fight()


if __name__ == "__main__":
    Solution().run()
