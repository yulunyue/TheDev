from common.algo.search.state import State, Action
from common.util.export import List, Dict
from .constant import C2
import random

N = 5


class PAction(Action):
    def __init__(self, src, action, dst=None):
        super().__init__(src, action, dst)
        self.rewards = []

    def add_preward(self, p, r, dst):
        self.rewards.append([p, r, dst])


class Mdp1State(State):
    P: Dict[str, int] = C2.Pi_1

    def make_actions(self, **kw):
        actions = []

        for pk, p in C2.P.items():
            f, a, d = pk.split("-")
            if int(f[1]) != self.state:
                continue
            name = f + "-" + a
            ac = PAction(self, a)
            for k, r in C2.R.items():
                if k.startswith(name):
                    ac.add_preward(p, r, int(k.split("-")[-1][-1]) - 1)
            if ac.rewards:
                actions.append(ac)
        return actions

    @classmethod
    def get_mrp_form_mdp(cls):
        ans = [[0] * N for _ in range(N)]
        for k, v in cls.P.items():
            s, t = k.split("-")
            s, t = int(s[1]) - 1, int(t[1]) - 1
            ans[s][t] = v
        return ans


class Mdp2State(Mdp1State):
    P = C2.Pi_2
