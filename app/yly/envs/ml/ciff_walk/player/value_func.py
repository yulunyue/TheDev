from common.algo.export import PolicyIteration, ValueIteration, Algo
from ..constant import C
from common.util.export import defaultdict, logger
from common.third_util.pt_table import PtTable
from ..env import CfState


class VFunc(ValueIteration):
    def reset(self):
        self.set_pi(defaultdict(lambda: {i: 1 for i in range(4)}))
        return super().reset()

    def get_qsa_value(self, qsalst):
        return max(qsalst)

    def log_value(self, diff):
        logger.debug(
            f"---log_value-----ep:{self.p_cnt}--diff:{diff}--\n{to_matrix(self.v)}"
        )

    def log_policy(self, pi):
        logger.debug(f"---log_policy------\n{to_matrix(pi)}")
