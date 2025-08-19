from common.algo.search.state import np, State, Action
from common.util.export import List, Dict
from .constant import C2
import random

N = 5


class MdpState(State):
    count = 0

    @classmethod
    def new(cls, state=None, **kw) -> "MdpState":
        if state is None:
            state = random.randint(1, 4)
        return super().new(state, **kw)

    def make_actions(self, depth=1, **kw):
        actions = dict()
        for a in C2.ACTIONS:
            key = f"s{self.state}-{a}"
            if key not in C2.R:
                continue
            for i in range(1, N + 1):
                pk = f"{key}-s{i}"
                if pk not in C2.P:
                    continue
                a = (
                    Action(self, key, MdpState.new(i))
                    .set_reward(C2.R[key])
                    .set_p(C2.P[pk])
                )
                actions[pk] = a
        return actions

    def get_pi_reawrd(self, pi):
        ret = 0
        for a in self.get_actions().values():
            ret += a.get_reward() * pi[a.action]
        return ret

    def get_done(self):
        return self.state == 5


def get_mrp_form_mdp(pi: Dict[str, int]):
    ans = [[0] * N for _ in range(N)]
    for k, v in pi.items():
        an, _ = k.split("-")
        s = MdpState.new(int(an[1]))
        for d in s.get_actions().values():
            ans[s.state - 1][d.dst.state - 1] += d.p * v
    return ans
