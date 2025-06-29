from .main import Bandit, BAN_ENV
from common.util.export import TestBase, logger, json
from common.algo.export import (
    ValueIteration,
    PolicyIteration,
    EpsilonGreedy,
    DecayingEpsilonGreedy,
    Ucb,
    ThompsonSampling,
    random_seed,
    Sarsa,
    np,
    Qlearning,
    AlphaBateSearch,
)


class TestBan(TestBase):
    def __init__(self):
        super().__init__()
        self.bs = Bandit(state="")
        BAN_ENV.load(10)

    def test_eg(self):
        eg = EpsilonGreedy().load()
        a = eg.search(self.bs)
        self.expect(a.action, BAN_ENV.max_idx)

    def test_ab(self, use_ab="use_ab"):
        ab = AlphaBateSearch().load(2, use_alpha_bate=use_ab == "use_ab")
        self.expect(ab.search(self.bs).action, BAN_ENV.max_idx, BAN_ENV.probs)

    def test_mc(self):
        pass


if __name__ == "__main__":
    random_seed(7)
    TestBan().run()
