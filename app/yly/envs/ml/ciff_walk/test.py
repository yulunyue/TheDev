from common.util.export import TestBase, logger
from .env import CfState, C
from .util.value_func import PiFunc, VFunc
from common.algo.export import random_seed, ValueIteration


class CfTest(TestBase):

    def run_policy(self):
        PiFunc().load().train(CfState)

    def run_value(self):
        VFunc().load().train(CfState)

    def debug(self):
        self.run_value()


if __name__ == "__main__":
    random_seed(0)
    CfTest().run()
