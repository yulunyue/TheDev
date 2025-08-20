from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, random, List, defaultdict
from common.algo.learn.base import Base


class MctsEasy(Base):
    def load(
        self, alpha=0.1, gamma=0.5, epsilon=1, num_episodes=500, mct_reward=None, **kw
    ):
        self.init_reward = mct_reward or defaultdict(int)
        return super().load(alpha, gamma, epsilon, num_episodes, **kw)

    def reset(self):
        self.vt = defaultdict(int)
        self.mct_reward = self.init_reward.copy()
        return self

    def update_state(self, s: State, score):
        self.g = self.gamma * self.g + score
        self.vt[s.state] += 1
        cv = self.mct_reward[s.state]
        nv = cv + (self.g - cv) / self.vt[s.state]
        self.mct_reward[s.state] = nv

    def feed_back_actions(self, actions: List[Action]):
        self.g = 0
        for i in range(len(actions) - 1, -1, -1):
            a = actions[i]
            r = a.get_reward()
            if r is not None:
                self.update_state(a.src, r)
            else:
                self.update_state(a.get_dst(), a.get_dst().get_reward())

        # logger.debug(f"---xxx---\n{actions}\n{dict(self.mct_reward)}\n{dict(self.vt)}")
