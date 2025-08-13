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
        self.b = Bandit()
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
        algo.reward_tmp_all = 0
        a = ALgoManage().set_state(self.b)
        a.train([algo], epochs=1)
        b = algo.get_max_action(self.b).action
        self.expect(
            # BAN_ENV.max_idx,
            b,
            BAN_ENV.max_idx,
            f"name:{algo.name}\nb:{self.b}",
        )
        logger.info(f"{algo.name}:{self.b}")
        self.d.draw_line(algo.rewards_record, title=algo.name)

    def debug(self):
        self.test_de()

    def exit(self):
        return self.d.save(self.get_temp_file(f"all.svg"))


if __name__ == "__main__":
    # random_seed(2)
    TestBan().run()
