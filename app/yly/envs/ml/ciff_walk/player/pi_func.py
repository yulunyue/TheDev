from common.algo.export import PolicyIteration, ValueIteration, Algo
from common.util.export import defaultdict, File, logger
from ..constant import C


class PiFunc(PolicyIteration):

    def reset(self):
        self.set_pi(defaultdict(lambda: [0.25] * 4))
        return super().reset()

    def view(self):
        return C.view(self)
