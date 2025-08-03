from common.algo.search.algo import State, np, random_select, Action
from .constant import C
from common.util.export import List, Dict


def computer(rewards, pi, gamma=0.5, **kw):
    reward = np.array(rewards).reshape((-1, 1))
    k = len(rewards)
    eye = np.eye(k, k)
    eye += -gamma * np.array(pi)
    r: np.ndarray = np.dot(np.linalg.inv(eye), reward)
    return r.reshape((1, -1))[0]


class MarkovRewardProcess:
    state_store: Dict[str, "MarkovRewardProcess"] = dict()
    n = len(C.STATE_VALUE)

    def action_size(self):
        return len(C.MRP_REWARD)

    def get_actions_score(self, chains, gamma=0.5):
        ret = 0
        for i in chains[::-1]:
            ret = gamma * ret + C.MRP_REWARD[i]
        return ret

    def berman(self, reward, gamma=0.5, **kw):
        ret = C.MRP_REWARD.copy()
        for i in range(self.n):
            for j in range(self.n):
                ret[i] += gamma * C.MRP_P[i][j] * reward[j]
        return ret
