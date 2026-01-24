from common.util.export import ToolBase, logger
from common.algo.export import Dqn, Qlearning, np, random_seed, DoubleDqn
from .env import CartPoleState
from .model.net import NetBase


class CartTool(ToolBase):
    uri = """
    https://hrl.boyuai.com/chapter/2/dqn%E6%94%B9%E8%BF%9B%E7%AE%97%E6%B3%95
"""

    def get_init_state(self):
        return CartPoleState()

    def get_moudle_cls(self):
        return NetBase

    def prepare(self, algo):
        self.s = self.get_init_state()
        if algo == "dqn2":
            self.al = DoubleDqn()
        else:
            self.al = Dqn()

    def train(self, train_epoll=500):
        dqn = self.al.load(
            train_epoll=int(train_epoll),
            learning_rate=2e-3,
            gamma=0.98,
            e_greed=0.01,
        ).set_model(self.get_moudle_cls(), target_update=10)
        dqn.train(self.s)
        logger.debug(dqn.draw_reward())

    def show(self):
        s = CartPoleState()
        logger.debug(s.show())

    def dev(self):
        pass

    def debug(self):
        self.dev()


if __name__ == "__main__":
    random_seed(0)
    CartTool().run()
