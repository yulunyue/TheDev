from common.algo.export import PolicyIteration, ValueIteration, Algo
from ..constant import C
from common.util.export import defaultdict, logger
from common.third_util.pt_table import PtTable
from ..env import CfState


def to_matrix(p):
    ret = []
    for i in range(C.nrow):
        ret.append([])
        for j in range(C.ncol):
            k = i * C.ncol + j
            if isinstance(p, Algo):
                s = CfState.new(k)
                v = "N"
                if not s.game_over():
                    v = p.take_action(s).action
            else:
                v = p.get(k, "")
            if isinstance(v, float):
                v = "%.3f" % (v)
            elif isinstance(v, list):
                v = ",".join(["%.2f" % (s) for s in v])
            elif isinstance(v, dict):
                v = "".join(C.ACS[k] if v[k] != 0 else "" for k in v)
            elif isinstance(v, int):
                v = C.ACS[v]
            ret[-1].append(v)
    p = PtTable().load_from_matrix(ret)
    return p.show()


class PiFunc(PolicyIteration):
    def reset(self):
        self.set_pi(defaultdict(lambda: [0.25] * 4))
        return super().reset()

    def log_value(self, diff):
        logger.debug(
            f"---log_value----round:{self.cnt}--ep:{self.p_cnt}--diff:{diff}--\n{to_matrix(self.v)}"
        )

    def log_policy(self, pi):
        logger.debug(f"---log_policy----round:{self.cnt}-----\n{to_matrix(pi)}")


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
