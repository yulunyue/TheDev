from common.util.export import TestBase, logger
from app.yly.algo.learn.export import CfState, Bandit
from common.algo.export import (
    ValueIteration,
    PolicyIteration,
    EpsilonGreedy,
    DecayingEpsilonGreedy,
    Ucb,
    ThompsonSampling,
    random_seed,
)


class TestLn(TestBase):
    def test_cf_value_iteration(self):
        s = CfState().load()
        v = ValueIteration().load()
        v.run(s)

    def test_cf_prun(self):
        v = PolicyIteration().load()
        num = v.run(CfState.all_states())
        logger.info(f"run {num}")

    def test_cf_policy_evaluation(self):
        p = PolicyIteration().load()
        states = CfState.all_states()
        cnt, diff_records = p.policy_evaluation(states)
        s = p.policy_improvement(states)
        logger.draw_line("record", diff_records)
        logger.info(CfState.to_str())

    def test_ban(self):
        bs = Bandit()
        for cls in [EpsilonGreedy, DecayingEpsilonGreedy, Ucb, ThompsonSampling]:
            c: EpsilonGreedy = cls()
            c.load().run(bs)
            self.expect_array(bs.probs, c.estimates)
            logger.draw_line(f"{cls.__name__}", c.regret_record)


if __name__ == "__main__":
    random_seed(3)
    TestLn().run()
