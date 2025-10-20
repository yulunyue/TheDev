from app.yly.envs.ml.cart_pole.export import CartPoleState, Net2
from common.util.export import TestBase, logger
from common.algo.export import Dqn, Qlearning, np


class TestCart(TestBase):
    def prepare(self, args=None):

        self.state = CartPoleState()
        self.dqn = Dqn().load(Net2().load())
        return super().prepare(args)

    def train(self):
        self.dqn.train(self.state)
        # self.dqn.search()
        # dqn.draw(self.get_temp_file("reawrd.svg"))

    def debug(self):
        pass

    def run_base(self):
        s = CartPoleState()
        logger.debug(s.show())


if __name__ == "__main__":
    TestCart().run()
