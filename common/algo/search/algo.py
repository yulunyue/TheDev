from common.third_util.ml.np_util import np
from common.algo.search.state import State, inf, Action
from common.algo.search.param import Params
from collections import deque
from collections import defaultdict
from common.util.export import (
    File,
    logger,
    get_log,
    get_dev_log,
    time,
    random,
    List,
    Dict,
    log,
)


def random_seed(v=1):
    logger.info(f"random_seed {v}")
    np.random.seed(v)
    random.seed(v)


def random_select(states, fn):
    rand, temp = np.random.rand(), 0
    for s in states:
        temp += fn(s)
        if temp > rand:
            return s


class Algo:

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__
        self.params = None

    def set_name(self, name):
        self.name = name
        return self

    def load(self):
        self.reset()
        return self

    def set_params(self, params):
        self.params: Params = params
        return self

    use_time = 0

    def search(self, state: "State", *args, last_a=None, **kw):
        if state.game_over():
            return state.get_best_action()
        self.reset()
        start_time = time.time()
        ret = self.search_best_action(state.reset(), *args, last_a=last_a, **kw)
        self.use_time = time.time() - start_time
        return ret

    def search_best_action(self, s: State, last_a: Action = None):
        pass

    def show(self):
        return f"---name:{self.get_name()}"

    model_file: File = None

    def set_model(self, model_file, new_model=False):
        self.model_file = File(f"data/model/{model_file}")
        if self.model_file.exists() and new_model:
            self.q = self.model_file.read_file()
        return self

    def get_best_action(self, state: "State", **kw) -> Action:
        max_value, max_a = -inf, []
        for a in state.get_sort_actions():
            r = self.get_action_reward(a)
            if r > max_value:
                max_value, max_a = r, [a]
            elif r == max_value:
                max_a.append(a)
        if max_a:
            return max_a[random.randint(0, len(max_a) - 1)]

    def get_action_reward(self, a: Action):
        return

    def take_action(self, state: "State") -> Action:
        pass

    def update_action(self, a: Action, **kwargs):
        pass

    def reset(self):
        return self

    def get_name(self):
        return self.name

    def actor(self):
        pass

    def set_train_epoll(self, train_epoll):
        self.train_epoll = train_epoll
        return self

    train_epoll = 1
    train_epoll_update = 0

    def train_before(self):
        pass

    def train(self, state: State):
        self.train_before()
        self.rewards = []
        start_time = time.time()
        from common.third_util.tqdm_util import tqdm

        logger.info(f"{self.show()} train_epoll:{self.train_epoll} begin trainging")
        for i in tqdm(range(self.train_epoll)):
            total_reward = self.train_one(i, state)
            self.rewards.append(total_reward)
            if self.train_epoll_update and (i + 1) % self.train_epoll_update == 0:
                self.train_update()
        self.use_time = time.time() - start_time
        logger.info(
            f"{self.get_name()} train_finish {self.use_time} to {self.model_file}"
        )
        self.finish_train()

    def train_update(self):
        pass

    def finish_train(self):
        self.draw_reward()

    def draw_reward(self):
        from common.third_util.view.draw import Draw

        path = f"data/algo/{self.get_name()}.svg"
        Draw().draw_line(self.rewards).save(path)

    max_train_round = 200

    def train_one(self, i, state: State):
        s = state.reset()
        r = 0
        self.actions: List[Action] = []
        self.steps = 0
        while not s.game_over() and self.steps <= self.max_train_round:
            a = self.take_action(s, i=i)
            a.do()
            r += a.get_reward()
            s = a.get_dst()
            self.update_action(a, idx=self.steps)
            self.actions.append(a)
            self.steps += 1
        return r

    def view(self):
        return self.show()


class RandomAlgo(Algo):
    def get_best_action(self, s: State, **kw):
        return s.get_random_action()


class BestAlgo(Algo):
    def get_best_action(self, s: State, **kw):
        return s.get_best_action()
