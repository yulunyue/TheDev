from app.yly.envs.ml.bandit.main import Bandit, BAN_ENV
from common.util.export import TestBase, json
from common.third_util.draw import Draw
from common.algo.export import (
    EpsilonGreedy,
    DecayingEpsilonGreedy,
    Ucb,
    ThompsonSampling,
    random_seed,
    Algo,
    ALgoManage,
    MctsEasy,
)


class TestBan(TestBase):

    def prepare(self):
        BAN_ENV.load()
        self.d = Draw()

    def test_eg(self):
        self.algo(EpsilonGreedy().load())

    def test_de(self):
        self.algo(DecayingEpsilonGreedy().load(epsilon=0.1))

    def test_ucb(self):
        self.algo(Ucb().load())

    def test_ts(self):
        self.algo(ThompsonSampling().load())

    def test_mcts(self):
        self.algo(MctsEasy().load())

    def algo(self, algo: EpsilonGreedy):
        b = Bandit()
        algo.train(b)
        self.expect(b.best_action.action, BAN_ENV.max_idx)
        self.d.draw_line(algo.rewards_record, title=algo.name)

    def debug(self):
        self.test_mcts()

    def exit(self):
        return self.d.save(self.get_temp_file(f"all.svg"))


if __name__ == "__main__":
    # random_seed(2)
    TestBan().run()
