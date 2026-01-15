from common.algo.search.algo import Algo, Action, State, np
from common.util.export import (
    get_log,
    logger,
    List,
    random,
    defaultdict,
    CT,
    ListUtil,
    File,
)


class Qlearning(Algo):
    def load(
        self, train_epoll=1000, e_greed=0.1, learning_rate=0.1, gamma=0.9, n_planning=0
    ):
        self.n_planning = n_planning
        self.lr = learning_rate
        self.train_epoll = train_epoll
        self.gamma = gamma
        self.e_greed = e_greed
        return super().load()

    def show(self):
        return f"---name:{self.get_name()} train_epoll:{self.train_epoll} e_greed:{self.e_greed}"

    def reset(self):
        self.q = dict()
        return self

    def calc_score(self, a: Action):
        return self.q.get(a.key, 0)

    def get_max_q_action(self, s: State) -> Action:
        scores = [self.calc_score(v) for v in s.get_sort_actions()]
        mx_scroe = max(scores)
        actions = ListUtil(s.get_sort_actions()).filter(
            lambda v: self.calc_score(v) == mx_scroe
        )
        if not actions:
            raise Exception(f"{s.show()},{len(s.get_sort_actions())}")
        return actions[random.randint(0, len(actions) - 1)]

    def take_action(self, s: State):
        actions = s.get_sort_actions()
        if random.random() < self.e_greed:
            return actions[random.randint(0, len(actions) - 1)]
        return self.get_max_q_action(s)

    def update_action(self, a0: Action, **kw):
        target = a0.get_reward()
        if not a0.get_dst().game_over():
            target += self.gamma * self.get_next_max_value(a0)
        self.q[a0.key] = self.calc_score(a0) + self.lr * (target - self.calc_score(a0))
        # logger.info(a0.show(self.q[a0.key]))

    def get_next_max_value(self, a0: Action):
        next_action_value = [
            self.calc_score(a) for a in a0.get_dst().get_sort_actions()
        ]
        next_max_q = max(next_action_value)
        if a0.src.mode == State.MAN2:
            return -next_max_q
        return next_max_q

    def train(self, state):
        super().train(state)
        if self.model_file is not None:
            self.model_file.write_file(self.q)

    def search_main(self, state, **kw):
        return self.get_max_q_action(state)
