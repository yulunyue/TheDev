from common.algo.export import ValueIteration


class ValueFunc(ValueIteration):
    def log_policy(self, pi: dict):
        keys = pi.keys()
        return super().log_policy(pi)
