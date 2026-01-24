from common.algo.export import Dqn
from ..model.net import NetBase


class DqnCart(Dqn):
    def load(
        self,
        train_epoll=1000,
        e_greed=0.01,
        learning_rate=0.002,
        gamma=0.9,
        n_planning=0,
    ):
        return (
            super()
            .load(train_epoll, e_greed, learning_rate, gamma, n_planning)
            .set_model(NetBase, target_update=10)
        )
