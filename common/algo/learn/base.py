from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, List


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
            actions = list(state.get_actions().values())
            return actions[np.random.randint(len(actions))]
        return self.get_max_action(state)

    def get_max_action(self, state: State) -> Action:
        actions = list(state.get_actions().values())
        return actions[np.argmax([a.get_reward() for a in actions])]

    def train(self, state_cls: State):
        self.reward_tmp_all = 0
        init_state = state_cls.new()
        self.reset()
        for _ in range(self.num_episodes):
            s = init_state.reset()
            actions: List[Action] = []
            while not s.get_done():
                ac = self.take_action(s)
                actions.append(ac)
                self.update_action(ac)
                self.reward_tmp_all += ac.get_regret()
                s = ac.get_dst()
            self.feed_back_actions(actions)
            self.rewards_record.append(self.reward_tmp_all)
        init_state.set_best_action(self.take_action(init_state))

    def feed_back_actions(self, actions: List[Action]):
        pass
