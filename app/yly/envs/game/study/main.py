from common.util.export import (
    ToolBase,
    logger,
    Module,
    random,
    List,
    log,
    logger,
    get_dev_log,
)
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
from .state import TestState


class SearchTool(ToolBase):
    def prepare(self):
        # self.s = TestState.make_test_state()
        self.s = TestState.new_random_state(24)
        self.al = ALgoManage().set_state(self.s)

    def print(self):
        log.debug(f"-----")
        s = TestState.new_random_state()

    def run_algo(self, al: Algo):
        a = al.search(self.s)
        lg = get_dev_log(f"data/search/{al.get_name()}")
        lg.debug(a.show())
        lg.debug(al.show())
        lg.debug(self.s.print_tree())

    def ad(self):
        self.run_algo(self.al.ad())

    def ab(self):
        self.run_algo(self.al.ab())

    def mc(self):
        self.run_algo(self.al.mc())

    def ql(self):
        pass

    def dev(self):
        self.ad()
        self.ab()

    def debug(self):
        self.mc()


if __name__ == "__main__":
    random_seed(7)
    SearchTool().run()
