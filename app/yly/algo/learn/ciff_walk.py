from common.algo.manage import (
    SolutionBase,
    View,
    bisect,
    defaultdict,
    Dict,
    List,
    MOD,
    inf,
    heapq,
    functools,
    logger,
)
from common.algo.learn.dqn import Dqn, Env, Algo, Action
from common.algo.learn.dyn import PolicyIteration, ValueIteration
import numpy as np

ACTIONS = [[0, -1], [-1, 0], [1, 0], [0, 1]]
ACS = ["<", "^", "v", ">"]


class CfState(Env):
    ncol = 12
    nrow = 4

    def __init__(self, key):
        super().__init__()
        self.state = key

    def get_nexts(self, *args):
        return self.actions

    def init_state(self):
        self.actions = []
        for i, a in enumerate(ACTIONS):
            y, x = self.state // 12, self.state % 12
            next_y = min(max(y + a[0], 0), self.nrow - 1)
            next_x = min(max(x + a[1], 0), self.ncol - 1)
            reward, done = -1, False
            next_state = next_y * 12 + next_x
            if y == self.nrow - 1 and x > 0:
                next_state, reward, done = self.state, 0, True
            elif next_y == self.nrow - 1 and next_x > 0:
                done = True
                if next_x != self.ncol - 1:
                    reward = -100
            self.actions.append(Action(i, get_state(next_state).set_done(done), reward))

    def new_state(self, i):
        return get_state(i)


ENV_MAP: Dict[str, CfState] = dict()


def get_state(s=12 * 3):
    if s not in ENV_MAP:
        ENV_MAP[s] = CfState(s)
        ENV_MAP[s].init_state()
    return ENV_MAP[s]


class Solution(SolutionBase):

    def get_cases(self):
        return [
            dict(name="va"),
        ]

    def get_algo(self, name):
        return dict(pi=PolicyIteration, dqn=Dqn, va=ValueIteration)[name](name)

    def init(self, name, *args, **kwargs):
        self.init_state = get_state()
        self.ai: Algo = self.get_algo(name).load(**kwargs)

    def print(self):
        self.log("Q_VALUE:")
        for i in range(CfState.nrow):
            tmp = []
            for j in range(CfState.ncol):
                tmp.append("%6.6s" % ("%.3f" % self.ai.v[i * CfState.ncol + j]))
            self.log(" ".join(tmp))
        self.log("ACTIONS")
        for i in range(CfState.nrow):
            tmp = []
            for j in range(CfState.ncol):
                tmp.append(ACS[np.argmax(self.ai.pi[i * CfState.ncol + j])])
            self.log(" ".join(tmp))

    def execute(self, **kw):
        self.log(self.ai.run(self.init_state))
        self.print()


if __name__ == "__main__":
    Solution().run()
