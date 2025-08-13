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
        self.actions: List[Action] = []
        ac = self.take_action(state)
        self.update_action(ac)
        state.set_best_action(ac)
        # logger.info(f"run_one {self.state_count}")
