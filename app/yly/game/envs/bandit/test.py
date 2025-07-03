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
    Algo,
)


class TestBan(TestBase):
    def prepare(self):
        BAN_ENV.load().use_pro(False)

    def test_all(self):
        self.test_algo(EpsilonGreedy().load())
        self.test_algo(DecayingEpsilonGreedy().load())
        self.test_algo(AlphaBateSearch().load(2))

    def test_dev(self):
        ab = AlphaBateSearch().load(2)
        self.test_algo(ab)

    def test_algo(self, algo: Algo):
        b = Bandit()
        a = algo.search(b)
        self.expect(
            a.action, BAN_ENV.max_idx, f"name:{algo.name} probs:{BAN_ENV.probs} b:{b}"
        )


if __name__ == "__main__":
    random_seed(0)
    TestBan().run()
