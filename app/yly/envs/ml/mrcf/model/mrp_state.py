from common.algo.search.algo import State, np, random_select, Action
from .constant import C1
from common.util.export import List, Dict


def computer(rewards, pi, gamma=0.5, **kw):
    reward = np.array(rewards).reshape((-1, 1))
    k = len(rewards)
    eye = np.eye(k, k)
    eye += -gamma * np.array(pi)
    r: np.ndarray = np.dot(np.linalg.inv(eye), reward)
    return r.reshape((1, -1))[0]


N = len(C1.STATE_VALUE)


class MrpAction(Action):
    def get_reward(self, **kwargs):
        return self.dst.reward


class MrpState(State):

    @classmethod
    def new(cls, state=None, **kw):
        if state is None:
            state = 0
        return super().new(state, **kw).set_reward(C1.MRP_REWARD[state])

    def make_actions(self, depth=1, **kw):
        actions = dict()
        for i in range(N):
            p = C1.MRP_P[self.state][i]
            if p == 0:
                continue
            nx = MrpState.new(i)
            actions[i] = MrpAction(self, i, nx).set_p(p)
        return actions

    def get_done(self):
        return self.state == 5
