from common.algo.search.algo import Algo, Action, State, np
from common.util.export import (
    get_log,
    logger,
    List,
    random,
    defaultdict,
)
from .sarse import Sarse


class Qlearning(Sarse):
    e_greed = 0.1

    def show(self):
        return f"---name:{self.get_name()} train_epoll:{self.train_epoll} e_greed:{self.e_greed}"

    def get_next_actions_reward(self, a: Action):
        return max(self.get_action_reward(a) for a in a.get_dst().get_sort_actions())

    def train_one(self, i, state):
        ret = super().train_one(i, state)
        # logger.info(self.get_model_file(f"t{i}.json").write_file(self.q))
        return ret
