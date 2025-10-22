from .eg import EpsilonGreedy, Bandit, Action


class DecayingEpsilonGreedy(EpsilonGreedy):

    def update_action(self, a, r):
        self.total_count += 1
        return super().update_action(a, r)
