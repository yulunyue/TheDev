from common.algo.export import Algo


class C:
    ACTIONS = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    ACS = ["^", "v", "<", ">"]
    ncol = 12
    nrow = 4
    INIT_SATTE = 36
    BEST_MAP = """---
vvvvvvvvvvvv
vvvvvvvvvvvv
>>>>>>>>>>>v
^###########
---"""

    @classmethod
    def view(self, al: Algo):
        from .env import CfState

        ret = []
        ret.append("---")
        for i in range(C.nrow):
            tmp = []
            for j in range(C.ncol):
                k = i * C.ncol + j
                a = al.search(CfState.new(k))
                acs = self.ACS[a.action] if a is not None else "#"
                tmp.append(acs)
            ret.append("".join(tmp))

        ret.append("---")
        return "\n".join(ret)
