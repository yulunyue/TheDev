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

    Algo,
)


class TestBan(TestBase):


    def test_all(self):
        self.test_algo(EpsilonGreedy().load())

        

    def test_dev(self, use_ab="use_ab"):
        ab = AlphaBateSearch().load(2, use_alpha_bate=use_ab == "use_ab")
        self.expect(ab.search(self.bs).action, BAN_ENV.max_idx, BAN_ENV.probs)

    def test_algo(self, algo:Algo):
        a = algo.search(Bandit())
        self.expect(a.action, BAN_ENV.max_idx)


if __name__ == "__main__":
    random_seed(7)
    TestBan().run()
