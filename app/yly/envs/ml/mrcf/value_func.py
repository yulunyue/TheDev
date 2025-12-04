from common.algo.export import ValueIteration, MctsEasy, Algo, Action
from common.util.export import defaultdict, logger


class Ocur(Algo):
    def load(self, gamma=0.5):
        self.gamma = gamma
        return super().load()

    def reset(self):
        self.rho = defaultdict(int)
        self.total_times = defaultdict(int)
        self.occur_times = defaultdict(lambda: defaultdict(int))
        return super().reset()

    def update_action(self, a: Action, idx, *args):
        self.total_times[idx] += 1
        self.occur_times[a.key][idx] += 1

    def train(self, state):
        ret = super().train(state)
        ts = sorted(self.total_times.keys(), reverse=True)
        for k, v in self.occur_times.items():
            for t in ts:
                self.rho[k] += self.gamma**t * v[t] / self.total_times[t]
        for k in self.rho:
            self.rho[k] = (1 - self.gamma) * self.rho[k]
        return ret


class Mcts(MctsEasy):
    pass
