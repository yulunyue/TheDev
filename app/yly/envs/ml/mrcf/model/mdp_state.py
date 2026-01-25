from common.algo.search.states.state import State, Action
from common.util.export import List, Dict, logger, random
from .constant import C2
import random

N = 5


class PAction(Action):
    def __init__(self, src, action, dst=None):
        super().__init__(src, action, dst)
        self.rewards = []

    def add_preward(self, p, r, dst):
        self.rewards.append([p, r, dst])
        return self

    def do(self):
        rd = rd2 = random.random()

        for p, r, d in self.rewards:
            if rd2 <= p:
                self.reward, self.dst = r, d
                return
            rd2 -= p
        raise Exception(self.src.state, rd, self.rewards)


class Mdp1State(State):
    P: Dict[str, int] = C2.Pi_1

    def __init__(self, state=None, player_id=0, depth=0):
        super().__init__(state, player_id, depth)
        if state is None:
            a = PAction(self, "s0-概率前往")
            self.P["s0-概率前往"] = 1
            for i in range(N - 1):
                a.add_preward(1 / (N - 1), 0, self.__class__.new(f"s{i+1}"))
            self.actions = [a]

    def game_over(self):
        return len(self.get_sort_actions()) == 0

    def get_random_action(self):
        rd = rx = random.random()
        for a in self.get_sort_actions():
            if rd <= self.P[a.action]:
                return a
            rd -= self.P[a.action]
        raise Exception(rx, [self.P[a.action] for a in self.get_sort_actions()])

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
