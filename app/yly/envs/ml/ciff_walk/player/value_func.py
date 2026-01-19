from common.algo.export import PolicyIteration, ValueIteration, Algo
from ..constant import C
from common.util.export import defaultdict, logger, File
from common.third_util.pt_table import PtTable
from ..env import CfState


class VFunc(ValueIteration):
    def reset(self):
        self.set_pi(defaultdict(lambda: [1] * 4))
        return super().reset()

    def get_qsa_value(self, qsalst):
        return max(qsalst)

    def view(self):
        return C.view(self)
