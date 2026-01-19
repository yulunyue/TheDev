from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, List


class Sarse(Algo):
    def load(self, n_step=1, **kw):
        self.n_step = n_step
        return super().load(**kw)

    def update_action(self, action: Action, **kw):
        if action.dst.game_over():
            return
        next_action = self.take_action(action.dst)
        self.update_td_action(action, next_action)

    def update_td_action(self, a0: Action, a1: Action):
        self.actions.append(a0)
        if len(self.actions) != self.n_step:
            return
        g = a1.value if a1 else 0
        for i in range(len(self.actions) - 1, -1, -1):
            a = self.actions[i]
            g = a.get_reward() + self.gamma * g
        s = self.actions.pop(0)
        td_error = g - s.value
        s.value += self.alpha * td_error

    def reset(self):
        self.actions: List[Action] = []
        return super().reset()
