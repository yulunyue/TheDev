from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, List
from common.algo.learn.base import Base


class MctsEasy(Base):
    def load(self, alpha=0.1, gamma=0.5, epsilon=1, num_episodes=500, **kw):
        return super().load(alpha, gamma, epsilon, num_episodes, **kw)

    def train(self, init_state: State, **kw):
        for _ in range(self.num_episodes):
            state = init_state.new()
            g = 0
            actions: List[Action] = []
            while not state.get_done():
                a = self.take_action(state)
                # self.reward_tmp_all += action.reward
                actions.append(a)
                state = a.get_dst()
            while actions:
                a = actions.pop()
                g = self.gamma * g + a.reward
                a.src.count += 1
                a.src.mct_reward = (
                    a.src.mct_reward + (g - a.src.mct_reward) / a.src.count
                )
