from common.algo.export import PolicyIteration
from ..constant import C
from common.util.export import defaultdict


class PiFunc(PolicyIteration):
    def load(self, num_episodes=500, theta=0.001, gamma=0.9):
        pi = defaultdict(lambda: [0.25] * 4)
        return super().load(pi, num_episodes, theta, gamma)

    def log_util(self, header, util):
        ret = [header]
        for i in range(C.nrow):
            tmp = []
            for j in range(C.ncol):
                k = i * C.ncol + j
                tmp.append(util(k))
            ret.append(" ".join(tmp))
        msg = "\n".join(ret)
        self.log(msg)

    def log_value(self, cnt, max_diff):
        self.log_util(
            f"----round:{cnt}----diff:{max_diff}",
            lambda k: "%6.6s" % ("%.3f" % self.v[k]),
        )

    def log_policy(self):
        def util(k):
            if k not in self.pi:
                return "oooo"
            return "".join(
                [C.ACS[i] if d > 0 else "o" for i, d in enumerate(self.pi[k])]
            )

        self.log_util("upgrade policy", util)


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
