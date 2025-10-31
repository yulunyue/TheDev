from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, List, random, defaultdict, CT, ListUtil


class Qlearning(Algo):
    def load(self, n_planning=0, train_epoll=100, e_greed=0.1, alpha=0.1, gamma=0.1):
        self.n_planning = n_planning
        self.alpha = alpha
        self.gamma = gamma
        self.train_epoll = train_epoll
        self.e_greed = e_greed
        self.all_actions = dict()
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

    def q_learning(self, a0: Action):
        next_max_value = 0
        for d in a0.get_dst().get_sort_actions():
            if self.q[d.key] > next_max_value:
                next_max_value = self.q[d.key]
        actions_value = a0.get_reward() + self.gamma * next_max_value
        self.q[a0.key] += self.alpha * actions_value

    def update_action(self, a0: Action):
        self.actions.append(a0)
        self.q_learning(a0)
        for _ in range(self.n_planning):
            s = random.choice(list(self.all_actions.values()))
            self.q_learning(s)

    def train(self, state: State):
        self.reset()
        for i in range(self.train_epoll):
            self.train_one(i, state)

    def train_one(self, i, state: State):
        s = state.reset()
        self.actions = []
        while not s.game_over:
            a = self.take_action(s)
            self.update_action(a)
            s = a.get_dst()

    def show(self):
        ret = []
        for k, v in self.q.items():
            ret.append(f"{k} = {v}")
        return super().show() + "\n" + "\n".join(ret)

    def search_main(self, state):
        return self.get_max_q_action(state)
