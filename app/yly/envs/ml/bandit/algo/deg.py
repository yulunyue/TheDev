from .eg import EpsilonGreedy, Bandit, Action


class DecayingEpsilonGreedy(EpsilonGreedy):

    def take_action(self, state: Bandit):
        r = super().take_action(state)
        self.total_count += 1
        return r
