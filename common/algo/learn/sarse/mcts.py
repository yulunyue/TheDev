from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, List, defaultdict
from common.algo.learn.base import Base


class MctsEasy(Base):
    def load(self, alpha=0.1, gamma=0.5, epsilon=1, num_episodes=500, **kw):
        return super().load(alpha, gamma, epsilon, num_episodes, **kw)

    def reset(self):
        self.vt = defaultdict(int)
        self.mct_reward = defaultdict(int)
        return self

    def feed_back_actions(self, actions: List[Action]):
        g = 0
        for i in range(len(actions) - 1, -1, -1):
            a = actions[i]
            g = self.gamma * g + a.get_reward()
            self.vt[a.src.state] += 1
            cv = self.mct_reward[a.src.state]
            nv = cv + (g - cv) / self.vt[a.src.state]
            self.mct_reward[a.src.state] = nv
