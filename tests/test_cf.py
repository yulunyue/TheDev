from common.util.export import TestBase, logger
from app.yly.envs.ml.ciff_walk.export import CfState, C, PiFunc, VFunc
from common.algo.export import random_seed, ValueIteration


class TestCf(TestBase):
    def prepare(self, args=None):
        self.pf = PiFunc().load()
        self.vf = VFunc().load()
        self.init_state = CfState.new(C.INIT_SATTE)
        # self.states = [v[1] for v in self.init_state.bfs().values()]
        return super().prepare(args)

    def run_policy(self):
        self.pf.train_all_states([])

    def run_value(self):
        self.vf.train(CfState)

    def debug(self):
        self.run_value()


if __name__ == "__main__":
    random_seed(0)
    TestCf().run()
