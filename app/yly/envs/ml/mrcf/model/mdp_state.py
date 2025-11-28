from common.algo.search.state import State, Action
from common.util.export import List, Dict, logger
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

    @property
    def idx(self):
        return int(self.state[-1]) - 1

    def make_actions(self, **kw):
        actions = []

        for action, r in C2.R.items():
            # logger.map(action=action, s=self.state, r=action.startswith(self.state))
            if not action.startswith(self.state):
                continue
            a = PAction(self, action)
            for k, p in C2.P.items():
                if k.startswith(action):
                    a.add_preward(p, r, self.__class__.new(k.split("-").pop()))

            actions.append(a)
        return actions

    @classmethod
    def get_mrp_form_mdp(cls):
        ans = [[0] * N for _ in range(N)]
        for i in range(N):
            s = cls.new(f"s{i+1}")
            for a in s.get_sort_actions():
                for p, r, ns in a.rewards:
                    ans[i][ns.idx] = cls.P[a.action] * p

        return ans


class Mdp2State(Mdp1State):
    P = C2.Pi_2
