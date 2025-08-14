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


class MrpState(State):

    def get_actions(self, depth=1, **kw):
        if self.actions is not None:
            return self.actions
        self.actions = dict()
        for i in range(N):
            p = 1
            if self.state is not None:
                p = C1.MRP_P[self.state][i]
            if p == 0:
                continue
            r = C1.MRP_REWARD[i]
            nx = MrpState.new(i).set_reward(r)
            self.actions[i] = Action(self, i, nx).set_p(p).set_reward(r)
        return self.actions
