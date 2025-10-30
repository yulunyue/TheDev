from app.yly.envs.ml.cart_pole.export import CartPoleState, Net2
from common.util.export import ToolBase, logger
from common.algo.export import Dqn, Qlearning, np


class CartTool(ToolBase):
    def prepare(self):
        self.state = CartPoleState()

    def dqn(self):
        dqn = Dqn().load(Net2().load())
        dqn.train(self.state)
        # self.dqn.search()
        # dqn.draw(self.get_temp_file("reawrd.svg"))

    def run_base(self):
        s = CartPoleState()
        logger.debug(s.show())


if __name__ == "__main__":
    CartTool().run()
