from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, List, random, defaultdict, File, log


class Sarse(Algo):
    def load(self, n_step=1, e_grade=0.1, model_file="q.json", **kw):
        self.n_step = n_step
        self.e_grade = e_grade
        self.gamma = 0.9
        self.alpha = 0.1
        self.model_file = self.get_model_file(model_file)
        self.best_q = dict()
        if self.model_file.exists():
            logger.info(self.model_file)
            self.best_q = self.model_file.read_file()

        return super().load(**kw)

    def train_before(self):
        self.q = self.best_q.copy()
        return self

    def reset(self):
        self.q = self.best_q.copy()
        return super().reset()

    def train_finish(self):
        logger.info(self.model_file.write_file(self.q))

    def update_action(self, action: Action, **kw):
        next_action = None
        if not action.dst.game_over():
            next_action = self.get_best_action(action.dst)
        self.update_td_action(action, next_action)

    def get_action_reward(self, a: Action):
        return self.q.get(a.key, 0)

    def update_td_action(self, a0: Action, a1: Action):

        # if len(self.actions) < self.n_step:
        #     return
        c = -1 if a0.src.mode == State.MAN2 else 1
        g = c * self.gamma * self.get_next_actions_reward(a1) if a1 else 0
        # for i in range(len(self.actions) - 2, self.steps, -1):
        #     a = self.actions[i]
        #     g = a.get_reward() + self.gamma * g
        a0_reward = self.get_action_reward(a0)
        td_error = a0.get_reward() + g - a0_reward
        self.q[a0.key] = a0_reward + self.alpha * td_error

    def get_next_actions_reward(self, a: Action):
        return self.get_action_reward(a)

    def take_action(self, state: State, i=0):
        # log.map(s=state.state, d=state.board.state)
        e_grade = 1 - self.e_grade * (i + 1) / self.train_epoll
        if random.random() < self.e_grade:
            return state.get_random_action()
        return self.get_best_action(state)

    def search_best_action(self, s, last_a=None):
        return self.get_best_action(s, last_a=last_a)
