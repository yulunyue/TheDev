from .env import PenduState
from common.util.export import TestBase, logger
from common.algo.export import Dqn, Qlearning, np


class TestPen(TestBase):

    def test_dqn(self):
        p = PenduState()
        dqn = Dqn().load(p.state_size(), 128, 11, cache="data/game/pen/main.pt")
        dqn.search(p)

    def test_debug(self):
        self.test_dqn()

    def test_base(self):
        s = PenduState()
        logger.info(s)


if __name__ == "__main__":
    TestPen().run()
