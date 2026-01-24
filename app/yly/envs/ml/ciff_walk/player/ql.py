from common.algo.export import random_seed, ValueIteration, Qlearning
from ..constant import C


class Ql(Qlearning):

    def view(self):
        return C.view(self)
