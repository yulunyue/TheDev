from common.util.export import TestBase, logger
from app.yly.envs.ml.cart_pole.player.dqn import DqnCart
from app.yly.envs.ml.cart_pole.env import CartPoleState


class TestDqn(TestBase):
    def test_train(self):
        s = CartPoleState()
        al = DqnCart().load(train_epoll=10)
        al.train(s)
