from common.third_util.ml.np_util import np
from .state import State, inf, Action
from .param import Params
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
    use_time = 0
    train_epoll = 1
    train_epoll_update = 0

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__
        self.params = None

    def set_name(self, name):
        self.name = name
        return self

    def set_options(self, train_epoll=None, train_epoll_update=None):
        if train_epoll is not None:
            self.set_train_epoll(int(train_epoll))
        if train_epoll_update is not None:
            self.train_epoll_update = int(train_epoll_update)
        return self

    def load(self):
        self.reset()
        return self

    def set_params(self, params):
        self.params: Params = params
        return self

    def search(self, state: "State", *args, last_a=None, **kw):
        state.reset()
        if state.game_over():
            return state.get_best_action()
        self.reset()
        start_time = time.time()
        ret = self.search_best_action(state, *args, last_a=last_a, **kw)
        self.use_time = time.time() - start_time
        return ret

    def search_best_action(self, s: State, last_a: Action = None):
        return self.get_best_action(s)

    def show(self):
        return f"---name:{self.get_name()}"

    def set_model(self, model_file, new_model=False) -> "Algo":
        raise NotImplementedError(model_file, new_model)

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

    def take_action(self, state: "State", i=0, **kw) -> Action:
        raise NotImplementedError("todo")

    def update_action(self, a: Action, **kwargs):
        pass

    def reset(self):
        return self

    def get_name(self):
        return self.name

    def set_train_epoll(self, train_epoll):
        self.train_epoll = train_epoll
        return self

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
                self.train_update_model(i, state)
        self.use_time = time.time() - start_time
        logger.info(f"{self.get_name()} train_finish {self.use_time}")
        self.train_finish()

    def train_update_model(self, i, state: State):
        raise NotImplemented()

    def train_finish(self):
        pass

    def get_model_file(self, name):
        return File(f"data/algo/{self.get_name()}/{name}")

    def draw_reward(self):
        from common.third_util.view.draw import Draw

        path = self.get_model_file("rewards.svg")
        Draw().draw_line(self.rewards).save(path)

    max_train_round = 200

    def train_one(self, i, state: State, op: "Algo" = None):
        s = state.reset()
        r = 0
        self.actions: List[Action] = []
        self.steps = 0
        while not s.game_over() and self.steps <= self.max_train_round:
            a = self.take_action(s, i=i)
            a.do()
            reward = a.get_reward()
            s = a.get_dst()
            r += reward
            self.update_action(a, idx=self.steps)
            self.actions.append(a)
            self.steps += 1
        return r

    def view(self):
        return self.show()


class RandomAlgo(Algo):
    def get_best_action(self, s: State, **kw):
        return s.get_random_action()


BestAlgo = Algo
