from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, List
from common.algo.learn.sarse.qlearning import Qlearning


class DynaQ(Qlearning):
    def load(self, n_planning=0, **kw):
        self.n_planning = n_planning
        self.model = dict()
        return super().load(**kw)

    def update_action(self, a0: Action):
        self.q_learning(a0)
        self.model[(a0.src.state, a0.action)] = a0
        for _ in range(self.n_planning):
            s = random.choice(list(self.model.values()))
            self.q_learning(s)
