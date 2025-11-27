from common.util.export import ToolBase, logger
from common.algo.export import Dqn, Qlearning, np, random_seed
from .env import CartPoleState
from .net import NetBase


class CartTool(ToolBase):
    def prepare(self):
        self.s = CartPoleState()

    def dqn(self):
        dqn = (
            Dqn()
            .load(
                train_epoll=500,
                learning_rate=2e-3,
                gamma=0.98,
                e_greed=0.01,
            )
            .set_model(NetBase, target_update=10)
        )
        dqn.train(self.s)
        logger.debug(dqn.show())
        # self.dqn.search()
        # dqn.draw(self.get_temp_file("reawrd.svg"))

    def run_base(self):
        s = CartPoleState()
        logger.debug(s.show())

    def dev(self):
        self.dqn()

    def debug(self):
        self.dev()


if __name__ == "__main__":
    random_seed(0)
    CartTool().run()
