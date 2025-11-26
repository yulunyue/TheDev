from common.algo.search.algo import Algo, Action, State, np
from common.util.export import (
    get_log,
    logger,
    List,
    random,
    defaultdict,
    CT,
    ListUtil,
    progress_bar,
)


class Qlearning(Algo):
    def load(
        self, n_planning=0, train_epoll=100, e_greed=0.1, learning_rate=0.1, gamma=0.9
    ):
        self.n_planning = n_planning
        self.lr = learning_rate
        self.train_epoll = train_epoll
        self.gamma = gamma
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

    def train_one(self, i, state):
        self.e_greed = 0.1 * (1 - i / self.train_epoll)
        return super().train_one(i, state)

    def q_learning(self, a0: Action):
        next_action_value = [self.q[a.key] for a in a0.get_dst().get_sort_actions()]
        next_max_q = max(next_action_value) if next_action_value else 0
        current_q = self.q[a0.key]
        r = a0.get_reward() + self.gamma * next_max_q - current_q
        self.q[a0.key] += self.lr * r
        # logger.info(a0.show(self.q[a0.key]))

    def update_action(self, a0: Action):
        self.q_learning(a0)
        for _ in range(self.n_planning):
            s = random.choice(list(self.all_actions.values()))
            self.q_learning(s)

    def show(self):
        ret = []
        for k, v in self.q.items():
            ret.append(f"{k} = {v}")
        return super().show() + "\n" + "\n".join(ret)

    def search_main(self, state):
        return self.get_max_q_action(state)
