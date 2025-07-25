from .main import Bandit, BAN_ENV
from common.util.export import TestBase, logger, json
from common.tool.draw import Draw
from common.algo.export import (
    EpsilonGreedy,
    DecayingEpsilonGreedy,
    Ucb,
    ThompsonSampling,
    random_seed,
    Algo,
)


class TestBan(TestBase):
    def prepare(self):
        BAN_ENV.load()
        self.prob_format = ", ".join(["%.2f" % v for v in BAN_ENV.probs])
        self.b = Bandit()
        self.d = Draw()
        logger.info(self.prob_format)

    def test_all(self):
        self.test_de()
        self.test_eg()
        self.test_ucb()
        self.test_ts()
        self.d.save(f"data/game/bandit/all.svg")

    def test_eg(self):
        self.test_algo(EpsilonGreedy().load())

    def test_de(self):
        self.test_algo(DecayingEpsilonGreedy().load(epsilon=0.1))

    def test_ucb(self):
        self.test_algo(Ucb().load())

    def test_ts(self):
        self.test_algo(ThompsonSampling().load())

    def test_algo(self, algo: Algo):
        a = algo.search(self.b)
        self.expect(
            a.action,
            BAN_ENV.max_idx,
            f"name:{algo.name}\nb:{self.b}",
        )
        logger.info(f"{algo.name}:{self.b}")
        self.d.draw_line(algo.rewards_record, title=algo.name)

    def test_debug(self):
        return self.test_eg()


if __name__ == "__main__":
    random_seed(3)
    TestBan().run()
