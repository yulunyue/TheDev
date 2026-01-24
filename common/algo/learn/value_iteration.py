from .policy_iteration import List, PolicyIteration, State


class ValueIteration(PolicyIteration):
    def get_qsa_value(self, qsalst):
        return max(qsalst)

    def train(self, state: State):
        states = state.bfs()
        self.policy_evaluation(0, states)
        self.policy_improvement(0, states)
        return self
