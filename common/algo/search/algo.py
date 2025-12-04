from common.third_util.np_util import np
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
    state_num = 0

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

    def search(self, state: "State", *args, **kw):
        self.reset()
        start_time = time.time()
        ret = self.search_main(state.reset(), algo=self, *args, **kw)
        self.use_time = time.time() - start_time
        return ret

    def info(self):
        return []

    def show(self):
        return "\n".join(
            [f"---name:{self.get_name()} use_time:{self.use_time}---"] + self.info()
        )

    def search_main(self, state: "State", algo=None) -> Action:
        pass

    def take_action(self, state: "State") -> Action:
        return state.get_random_action()

    def update_action(self, a: Action, *args):
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

    def train(self, state: State):
        self.reset()
        self.rewards = []
        start_time = time.time()
        from common.third_util.tqdm_util import tqdm

        logger.info("begin trainging")
        for i in tqdm(range(self.train_epoll)):
            total_reward = self.train_one(i, state)
            self.rewards.append(total_reward)
            if self.train_epoll >= 10 and (i + 1) % (self.train_epoll // 10) == 0:
                logger.map(Episode=i, TotalReward=sum(self.rewards) / len(self.rewards))
        self.use_time = time.time() - start_time

    def train_one(self, i, state: State):
        s = state.reset()
        r = 0
        self.actions: List[Action] = []
        self.steps = 0
        while not s.game_over():
            a = self.take_action(s)
            a.do()
            r += a.get_reward()
            s = a.get_dst()
            self.actions.append(a)
            self.update_action(a, idx=len(self.actions) - 1)
            self.steps += 1
        return r


class RandomAlgo(Algo):
    def search_main(self, s: State, **kw):
        return s.get_random_action()
