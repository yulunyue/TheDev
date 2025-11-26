from common.util.export import ToolBase, logger
from .env import CfState, C
from .util.value_func import PiFunc, VFunc, to_matrix
from .util.study_replay import RealTimeValueIteration
from common.algo.export import random_seed, ValueIteration, Qlearning


class CfTool(ToolBase):
    def prepare(self, *args, **kw):
        self.s: CfState = CfState.new(C.INIT_SATTE)

    def run_policy_all_state(self):
        f = PiFunc().load()
        f.train_all_states(self.s.bfs())

    def run_value_all_state(self):
        f = VFunc().load()
        f.train_all_states(self.s.bfs())

    def run_study_replay(self):
        f = RealTimeValueIteration().load()
        f.train(self.s)

    def run_ql(self):
        f = Qlearning().load(train_epoll=1000)
        f.train(self.s)
        logger.debug(to_matrix(f))

    def dev(self):
        self.run_ql()

    def debug(self):
        self.dev()


if __name__ == "__main__":
    random_seed(0)
    CfTool().run()
