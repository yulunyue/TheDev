from .qlearning import Qlearning, Action


class Qlearning2(Qlearning):

    def get_next_max_value(self, a0: Action):
        next_action_value = [
            -self.calc_score(a) for a in a0.get_dst().get_sort_actions()
        ]  # 2人博弈最大最小
        next_max_q = max(next_action_value)
        return next_max_q
