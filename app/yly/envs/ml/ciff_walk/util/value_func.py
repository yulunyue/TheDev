from common.algo.export import PolicyIteration
from ..constant import C
from common.util.export import defaultdict, logger
from common.third_util.pt_table import PtTable
from ..env import CfState


class PiFunc(PolicyIteration):
    def reset(self):
        self.set_pi(defaultdict(lambda: [0.25] * 4))
        return super().reset()

    def log_value(self, diff):
        logger.debug(
            f"---log_value----round:{self.cnt}--ep:{self.p_cnt}--diff:{diff}--\n{self.to_matrix(self.v)}"
        )

    def log_policy(self):
        logger.debug(
            f"---log_policy----round:{self.cnt}-----\n{self.to_matrix(self.pi)}"
        )

    def to_matrix(self, p):
        ret = []
        for i in range(C.nrow):
            ret.append([])
            for j in range(C.ncol):
                k = i * C.ncol + j
                v = p.get(k, None)
                if isinstance(v, float):
                    v = "%.3f" % (v)
                elif isinstance(v, list):
                    v = ",".join(["%.2f" % (s) for s in v])
                ret[-1].append(v)
        p = PtTable().load_from_matrix(ret)
        return p.show()


class VFunc(PiFunc):
    def load(self, num_episodes=500, theta=0.001, gamma=0.9):
        pi = defaultdict(lambda: [1] * 4)
        return PolicyIteration.load(self, pi, num_episodes, theta, gamma)

    def get_qsa_value(self, qsalst):
        return max(qsalst)

    def train(self, state_cls):
        states = state_cls.new().bfs().values()
        self.policy_evaluation(states)
        self.policy_improvement(states)
        return self
