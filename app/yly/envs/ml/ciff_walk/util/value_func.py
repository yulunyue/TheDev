from common.algo.export import PolicyIteration
from ..constant import C
from common.util.export import defaultdict, logger
from common.third_util.pt_table import PtTable
from ..env import CfState


class PiFunc(PolicyIteration):
    def load(self, num_episodes=500, theta=0.001, gamma=0.9):
        pi = defaultdict(lambda: [0.25] * 4)
        return super().load(pi, num_episodes, theta, gamma)

    def policy_evaluation(self, states, *args):
        cnt = super().policy_evaluation(states, *args)
        self.log(f"cnt:{cnt} states:{len(states)}")
        return cnt

    def log(self, msg):
        logger.debug(msg)
        p = PtTable().load_from_matrix(self.to_matrix(lambda v: "%.2f" % self.v[v]))
        logger.debug(p.show())

    def to_matrix(self, util):
        ret = []
        for i in range(C.nrow):
            ret.append([])
            for j in range(C.ncol):
                k = i * C.ncol + j
                ret[-1].append(util(k))
        return ret


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
