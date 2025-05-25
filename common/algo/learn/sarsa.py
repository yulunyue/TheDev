from common.algo.search.algo import Algo, Action, State, np


class Sarsa(Algo):
    def load(
        self,
        alpha=0.1,
        gamma=0.9,
        epsilon=0.1,
        use_cache=False,
        max_t=-1,
        num_episodes=1000,
    ):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        return super().load(use_cache, max_t, num_episodes)

    def search_main(self, state, **kw):
        if np.random.random() < self.epsilon:
            action = np.random.randint(len(self.actions))
        else:
            action = np.argmax(self.q_tables[state])
        return action

    def run(self, state: State, **kw):
        states = state.all_states()
        self.actions = states[0].get_actions_all()
        self.q_tables = [[[0] * len(self.actions)] for s in states]
        state.reset()
        last_action = None
        while not state.done:
            action = self.search(state)
            self.update(last_action, action)
            last_action = action
            state = action.dst

    def update(self, a0: Action, a1: Action):
        if a0 is None:
            return
        r = a1.dst.reward + a1.reward
        q1 = self.q_tables[a1.dst.state, a1.action]
        q2 = self.q_tables[a0.dst.state, a0.action]
        self.q_tables[]
        # td_error = r + self.gamma * self.q_tables[action.dst.state, action]
