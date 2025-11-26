from common.algo.export import State, np, Action
from .constant import C1
from common.util.export import List, Dict
import random


def computer(rewards, pi, gamma=0.5, **kw):
    reward = np.array(rewards).reshape((-1, 1))
    k = len(rewards)
    eye = np.eye(k, k) - gamma * np.array(pi)
    r: np.ndarray = np.dot(np.linalg.inv(eye), reward)
    return r.reshape((1, -1))[0]


N = len(C1.STATE_VALUE)


class MrpAction(Action):

    def __repr__(self):
        return f"{self.action}:{self.get_reward()}:{self.p}"


class MrpState(State):

    @classmethod
    def new(cls, state=0, **kw) -> "MrpState":
        return super().new(state, **kw)

    def make_actions(self, depth=1, **kw):
        actions = []
        for i in range(N):
            p = C1.MRP_P[self.state][i]
            nx = MrpState.new(i)
            a = MrpAction(self, i, nx).set_p(p).set_reward(C1.MRP_REWARD[i])
            actions.append(a)
        return actions

    def get_done(self):
        return self.state == 5

    def get_reward_by_actions(self, chains, gamma):
        g = 1
        r = 0
        s = self
        for a in chains:
            ac = s.get_action(a - 1)
            r += ac.get_reward() * g
            s = ac.get_dst()
            g *= gamma
        return r
