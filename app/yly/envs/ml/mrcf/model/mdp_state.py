from common.algo.search.state import State, Action
from common.util.export import List, Dict
from .constant import C2
import random

N = 5


class MdpState(State):
    count = 0

    @classmethod
    def new(cls, state=None, **kw) -> "MdpState":
        if state is None:
            state = 0
        return super().new(state, **kw)

    def make_actions(self, depth=1, **kw):
        actions: Dict[str, PAction] = dict()
        if self.state is None:
            return {
                i: Action(self, i, MdpState.new(i + 1)).set_reward(0) for i in range(N)
            }
        for pk, p in C2.P.items():
            f, a, d = pk.split("-")
            if int(f[1]) != self.state:
                continue
            name = f + "-" + a
            if name not in actions:
                actions[name] = PAction(self, name).set_reward(C2.R[name])
            actions[name].add_dst(MdpState.new(int(d[1])), p)
        return actions

    def get_pi_reawrd(self, pi):
        ret = self.get_reward()
        for a in self.get_actions().values():
            ret += a.get_reward() * pi[a.action]
        return ret

    def get_done(self):
        return self.state == 5


def get_mrp_form_mdp(pi: Dict[str, int]):
    ans = [[0] * N for _ in range(N)]
    for k, v in pi.items():
        a1, _ = k.split("-")
        s = MdpState.new(int(a1[1]))
        ac: PAction = s.get_action(k)
        for a, p in ac.dst_p.values():
            ans[s.state - 1][a.state - 1] += p * v
    return ans
