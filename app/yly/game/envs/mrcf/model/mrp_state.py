from common.algo.search.algo import State, np, random_select, Action
from .constant import C
from common.util.export import List, Dict


class MrpState(State):
    state_store: Dict[str, "MrpState"] = dict()

    @classmethod
    def new(cls, state) -> "MrpState":
        if state not in cls.state_store:
            cls.state_store[state] = cls(state)
        return cls.state_store[state]

    def get_actions(self, depth=1, **kw):
        if self.actions:
            return self.actions
        for i in range(self.action_size()):
            self.actions[i] = Action(self, i, self.__class__.new(i))
        return self.actions

    def action_size(self):
        return len(C.MRP_REWARD)

    def get_actions_score(self, chains, gamma=0.5):
        ret = 0
        for i in chains[::-1]:
            ret = gamma * ret + C.MRP_REWARD[i]
        return ret

    # def computer(self, gamma=0.5, **kw):
    #     reward = np.array(self.reward).reshape((-1, 1))
    #     eye = np.eye(self.K, self.K) - gamma * self.P
    #     return np.dot(np.linalg.inv(eye), reward)
