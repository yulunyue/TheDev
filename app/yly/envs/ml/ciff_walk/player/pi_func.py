from common.algo.export import PolicyIteration, ValueIteration, Algo


class PiFunc(PolicyIteration):
    def reset(self):
        self.set_pi(defaultdict(lambda: [0.25] * 4))
        return super().reset()
