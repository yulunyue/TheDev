from common.util.export import TestBase, logger
from app.yly.algo.learn.ciff_walk import CfState
from common.algo.export import ValueIteration, PolicyIteration


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
        logger.info(f"policy_evaluation: {cnt}轮, {s}")
        logger.draw_line("record", diff_records)
        # logger.info([cnt, values])

    def exit(self):
        logger.info(CfState.to_str())


if __name__ == "__main__":
    TestLn().run()
