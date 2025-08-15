from .main import Bandit, BAN_ENV
from common.util.export import TestBase, logger, json
from common.third_util.export import Draw
from common.algo.export import (
    EpsilonGreedy,
    DecayingEpsilonGreedy,
    Ucb,
    ThompsonSampling,
    random_seed,
    Algo,
    ALgoManage,
)


class TestBan(TestBase):

    def prepare(self):
        BAN_ENV.load()
        self.prob_format = ", ".join(["%.2f" % v for v in BAN_ENV.probs])
        self.d = Draw()
        logger.info(self.prob_format)

    def test_eg(self):
        self.algo(EpsilonGreedy().load())

    def test_de(self):
        self.algo(DecayingEpsilonGreedy().load(epsilon=0.1))

    def test_ucb(self):
        self.algo(Ucb().load())

    def test_ts(self):
        self.algo(ThompsonSampling().load())

    def algo(self, algo: EpsilonGreedy):
        algo.train(Bandit)
        logger.info(f"{algo.name} {algo.rewards_record[-1]}")
        self.d.draw_line(algo.rewards_record, title=algo.name)

    def debug(self):
        self.test_ucb()

    def exit(self):
        return self.d.save(self.get_temp_file(f"all.svg"))


if __name__ == "__main__":
    # random_seed(2)
    TestBan().run()
