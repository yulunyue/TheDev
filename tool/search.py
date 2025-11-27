from common.util.export import ToolBase, logger, Module, random, List, log, logger
from common.algo.export import (
    AbState,
    AbDev,
    Algo,
    Action,
    State,
    MctsSearch,
    ALgoManage,
    random_seed,
)
from common.tool.export import ThreadRecord
from app.yly.envs.game.study.state import TestState


class SearchTool(ToolBase):
    def prepare(self):
        self.al = ALgoManage()

    def print(self):
        s = TestState.make_test_state()
        log.debug(s.print_tree())
        log.debug(f"-----")
        s = TestState.new_random_state()
        log.debug(s.print_tree())

    def random(self):
        pass

    def mc(self, cls=None):
        self.al.mc().search(s)

    def ql(self, cls=""):
        s: State = get_s(cls)
        logger.debug(s.print_tree())
        algo = self.al.ql()
        algo.train(s)
        logger.debug(algo.show())

    def dev(self):
        self.print()


if __name__ == "__main__":
    random_seed(7)
    SearchTool().run()
