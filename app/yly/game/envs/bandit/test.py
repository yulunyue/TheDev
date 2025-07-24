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
        BAN_ENV.load().use_pro(True)
        self.prob_format = ",  ".join(["%.2f" % v for v in BAN_ENV.probs])
        self.b = Bandit()
        logger.info(self.prob_format)

    def test_all(self):
        self.test_algo(EpsilonGreedy().load())
        # self.test_algo(DecayingEpsilonGreedy().load())
        # self.test_algo(Ucb().load())
        # self.test_algo(ThompsonSampling().load())

    def test_algo(self, algo: Algo):
        a = algo.search(self.b)
        self.expect(
            a.action,
            BAN_ENV.max_idx,
            f"name:{algo.name}\nb:{self.b}",
        )
        store_path = f"data/game/bandit/{algo.name}.svg"
        Draw().draw_line(algo.rewards_record).save(store_path)

    def test_debug(self):
        return self.test_all()


if __name__ == "__main__":
    random_seed(3)
    TestBan().run()
