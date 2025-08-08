from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, List


class Base(Algo):
    def load(self, alpha=0.1, gamma=0.9, epsilon=0.01, num_episodes=500, **kw):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.num_episodes = num_episodes
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

    def search_main(self, state: State):
        self.rewards_record = []
        self.reward_tmp_all = 0
        self.round = 0
        while self.round < self.num_episodes:
            self.run_one(state)
            self.rewards_record.append(self.reward_tmp_all)
            self.round += 1
        state.set_best_action(self.get_max_action(state))
        # logger.map(round=self.round, reward=self.reward_tmp_all)

    def draw(self, path):
        from common.tool.export import Draw

        Draw().draw_line(self.reward_tmp_all).save(path)

    def run_one(self, state: State):
        state = state.reset()
        self.state_count = 0
        while not state.get_done():
            a = self.take_action(state)
            ac = state.get_action(a.action)
            self.reward_tmp_all += ac.get_reward()
            self.update_action(ac)
            state = ac.dst
            self.state_count += 1
        # logger.info(f"run_one {self.state_count}")
