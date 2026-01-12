from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, List, random, defaultdict, CT, ListUtil


class Qlearning(Algo):
    def load(
        self, train_epoll=100, e_greed=0.1, learning_rate=0.1, gamma=0.9, n_planning=0
    ):
        self.n_planning = n_planning
        self.lr = learning_rate
        self.train_epoll = train_epoll
        self.gamma = gamma
        self.e_greed = e_greed
        self.q = defaultdict(int)
        return super().load()

    def reset(self):
        self.q = defaultdict(int)
        return self

    def get_max_q_action(self, s: State) -> Action:
        def score(a: Action):
            return self.q[a.key]

        return ListUtil(s.get_sort_actions()).max(score)[1]

    def take_action(self, s: State):
        actions = s.get_sort_actions()
        if random.random() < self.e_greed:
            return actions[random.randint(0, len(actions) - 1)]
        return self.get_max_q_action(s)

    def train_one(self, i, state):

        return super().train_one(i, state)

    def update_action(self, a0: Action, **kw):
        next_action_value = [self.q[a.key] for a in a0.get_dst().get_sort_actions()]
        next_max_q = max(next_action_value) if next_action_value else 0
        r = a0.get_reward() + self.gamma * next_max_q - self.q[a0.key]
        self.q[a0.key] += self.lr * r
        # logger.info(a0.show(self.q[a0.key]))

    def show(self):
        ret = []
        for k, v in self.q.items():
            ret.append(f"{k} = {v}")
        return super().show() + "\n" + "\n".join(ret)

    def search_main(self, state, **kw):
        return self.get_max_q_action(state)
