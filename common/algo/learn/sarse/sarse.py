from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, List
from common.algo.learn.base import Base


class Sarsa(Base):
    def load(self, **kw):
        self.n_step = 1
        return super().load(**kw)

    def run_one(self, init_state: State, **kw):
        state: State = init_state
        action = self.take_action(state)
        self.actions: List[Action] = []
        while action:
            action = self.do_action(action)

    def do_action(self, action: Action, **kw):
        self.reward_tmp_all += action.reward
        next_action = self.take_action(action.dst)
        self.update_2action(action, next_action)
        if action.dst.done:
            return
        return next_action

    def update_2action(self, a0: Action, a1: Action):
        self.actions.append(a0)
        if len(self.actions) != self.n_step:
            return

        g = a1.value if a1 else 0
        done = a1 and a1.dst.done
        for i in range(len(self.actions) - 1, -1, -1):
            s = self.actions[i]
            g = s.reward + self.gamma * g
            # if done and i > 0:
            #     s.value += self.alpha * (g - s.value)
        s = self.actions.pop(0)
        td_error = g - s.value
        s.value += self.alpha * td_error
        if a0.src.state == 35:
            logger.debug(f"{a0.src}")
