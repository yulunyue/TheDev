from .env import CartPoleState
from common.util.export import TestBase, logger
from common.algo.export import Dqn, Qlearning, np


class TestCart(TestBase):

    def run_dqn(self):
        dqn = Dqn().load(4, 128, 2, num_episodes=400)  # cache="data/game/cart/main.pt")
        dqn.search(CartPoleState())
        dqn.draw(self.get_temp_file("reawrd.svg"))

    def test_debug(self):
        pass

    def test_base(self):
        s = CartPoleState()
        logger.info(s)


if __name__ == "__main__":
    TestCart().run()
