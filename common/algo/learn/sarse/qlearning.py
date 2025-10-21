from common.algo.search.algo import Algo, Action, State, np
from common.util.export import get_log, logger, List


class Qlearning(Algo):

    def do_action(self, a: Action):
        self.reward_tmp_all += a.reward
        self.update_action(a)
        return self.take_action(a.dst)

    def q_learning(self, a0: Action):
        actions_value = [a.get_reward() for a in a0.dst.get_actions().values()]
        if actions_value:
            action_value = max(actions_value)
        else:
            action_value = 0
        a0_value = a0.get_data("value", 0)
        td_error = a0.reward + self.gamma * action_value - a0_value
        a0.set_data("value", a0_value + self.alpha * td_error)

    def update_action(self, a0):
        self.q_learning(a0)
