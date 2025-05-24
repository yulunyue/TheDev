from common.algo.search.algo import Algo, Action, State


class Sarsa(Algo):
    def load(self, use_cache=False, max_t=-1, num_episodes=1000):
        return super().load(use_cache, max_t, num_episodes)

    def run(self, state: State):
        self.q_tables = [[[0] * len(s.get_actions_all())] for s in state.all_states()]
        state.reset()
        while not state.done:
            action = self.search(state)
            state = action.dst
