from common.util.export import ToolBase, logger
from .env import CfState, C
from .util.value_func import PiFunc, VFunc
from common.algo.export import random_seed, ValueIteration


class CfTool(ToolBase):
    def prepare(self, *args, **kw):
        self.s = CfState.new(C.INIT_SATTE)

    def run_policy_all_state(self):
        f = PiFunc().load()
        f.train_all_states(self.s.bfs())

    def run_value(self):
        f = ValueIteration().load()
        f.train_all_states(self.init_state.bfs())
        logger.debug(v.show())

    def run_all(self):
        self.run_policy()
        self.run_value()

    def debug(self):
        self.run_value()


if __name__ == "__main__":
    random_seed(0)
    CfTool().run()
