from common.algo.export import ValueIteration, MctsEasy


class ValueFunc(ValueIteration):
    def log_policy(self, pi: dict):
        keys = pi.keys()
        return super().log_policy(pi)


class Mcts(MctsEasy):
    pass
