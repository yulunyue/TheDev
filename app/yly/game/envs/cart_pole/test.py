from .env import CP_ENV, CartPoleState
from common.util.export import TestBase, logger
from common.algo.export import Dqn, Qlearning, np


class TestCart(TestBase):
    def __init__(self):
        super().__init__()

    def test_dev(self):
        dqn = Dqn().load()
        dqn.search(CartPoleState.get_init_state())
        logger.info(np.mean(dqn.rewards_record[:-10]))


if __name__ == "__main__":
    TestCart().run()
