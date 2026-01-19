from common.algo.export import random_seed, ValueIteration, Qlearning
from ..constant import C


class Ql(Qlearning):
    def load(
        self, train_epoll=100, e_greed=0.1, learning_rate=0.1, gamma=0.9, n_planning=0
    ):
        self.default_e = e_greed
        self.set_model("ciff_walk.json", True)
        return super().load(train_epoll, e_greed, learning_rate, gamma, n_planning)

    def train_one(self, i, state):
        self.e_greed = 0.1 * (1 - i / self.train_epoll)
        return super().train_one(i, state)

    def view(self):
        return C.view(self)
