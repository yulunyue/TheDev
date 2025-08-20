from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, List
import random


class Base(Algo):

    def load(self, alpha=0.1, gamma=0.9, epsilon=0.01, num_episodes=5000, **kw):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.num_episodes = num_episodes
        self.rewards_record = []
        return super().load(**kw)

    def can_epsilon(self):
        return np.random.random() < self.epsilon

    def take_action(self, state: State, **kw):
        if self.can_epsilon():
            return self.get_random_action(state)
        return self.get_max_action(state)

    def train(self, init_state: State, max_round=2000):
        self.reward_tmp_all = 0
        self.reset()
        for _ in range(self.num_episodes):
            s = init_state.reset()
            actions: List[Action] = []
            tmp_round = max_round
            while not s.get_done() and tmp_round:
                ac = self.take_action(s)
                actions.append(ac)
                self.update_action(ac)
                self.reward_tmp_all += ac.get_regret()
                s = ac.get_dst()
                tmp_round -= 1
            self.feed_back_actions(actions)
            self.rewards_record.append(self.reward_tmp_all)
        init_state.set_best_action(self.take_action(init_state))

    def feed_back_actions(self, actions: List[Action]):
        pass

    def search_main(self, state: State):
        self.max_actions = []
        self.max_score = float("-inf")

        def dfs(s: State, actions):
            next_actions = list(s.get_actions().values())
            if s.get_done() or not next_actions:
                score = self.get_actions_backend_score()
                if score > self.max_score:
                    self.max_score = score
                    self.max_actions = actions
                return
            for n in next_actions:
                dfs(n.get_dst(), actions + [n])

        dfs(state, [])
        return self.max_actions

    def get_actions_backend_score(self, actions: List[Action]):
        ret = 0
        for a in actions:
            ret = ret * self.gamma + a.get_reward() * a.p
        return ret
