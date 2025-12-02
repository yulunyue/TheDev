from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, random, List, defaultdict


class MctsEasy(Algo):
    def load(self, gamma):
        self.gamma = gamma
        return super().load()

    def reset(self):
        self.ns = defaultdict(int)
        self.vs = defaultdict(int)
        return self

    def train_one(self, i, state):
        r = super().train_one(i, state)
        g = 0
        for a in self.actions[::-1]:
            g = self.gamma * g + a.get_reward()
            self.ns[a.src.state] += 1
            self.vs[a.src.state] += (g - self.vs[a.src.state]) / self.ns[a.src.state]
        return r
