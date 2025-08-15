from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, List
from common.algo.learn.base import Base


class MctsEasy(Base):
    def load(self, alpha=0.1, gamma=0.5, epsilon=1, num_episodes=500, **kw):
        return super().load(alpha, gamma, epsilon, num_episodes, **kw)

    def feed_back_actions(self, actions: List[Action]):
        g = 0
        for i in range(len(actions) - 1, -1, -1):
            a = actions[i]
            g = self.gamma * g + a.reward
            a.src.count += 1
            a.src.mct_reward = a.src.mct_reward + (g - a.src.mct_reward) / a.src.count
