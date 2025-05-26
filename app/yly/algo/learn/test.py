from common.util.export import TestBase, logger, json
from app.yly.algo.learn.export import CfState, Bandit, Flvo
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
)


class TestLn(TestBase):

    def test_cfsarsa(self):
        s = Sarsa().load(num_episodes=50)
        rewards = []
        for i in range(10):
            rewards += s.run(CfState)
            logger.info(f"---{i}-- rewards:{np.mean(rewards[-10:])}")
        logger.draw_line("record", rewards)
        logger.info(len(rewards))
        logger.info(CfState.to_str())

    def test_flv0(self):
        # PolicyIteration().load().run(Flvo)
        Flvo.get_env()
        # ValueIteration().load().run(Flvo)

    def test_cfpr(self):
        PolicyIteration().load().run(CfState)

    def test_cfpv(self):
        ValueIteration().load().run(CfState)

    def test_cfpe(self):
        p = PolicyIteration().load()
        p.policy_evaluation(CfState)
        p.policy_improvement(CfState)
        v1 = json.loads(
            "[-27.238559676619346, -28.510206246429455, -29.62885270244113, -30.305628122512452, -30.63180044115316, -30.71290352575707, -30.576247758044943, -30.147026390044594, -29.224052962725274, -27.478407211415796, -24.65095855211554, -21.452783239853783, -33.6318737150897, -36.893230087142776, -38.79777435746743, -39.68392452942374, -40.0493986760689, -40.13912693311535, -40.01645050280487, -39.597576201305145, -38.59325411177045, -36.330852853611376, -31.53565514170566, -23.347152140868065, -47.269744178720174, -58.588300742368254, -61.78662689369652, -62.77814358941198, -63.10031193173464, -63.175112719696, -63.09561179906289, -62.790108249415496, -61.93065649443827, -59.42067040315814, -51.38701026633216, -22.98702501042819, -66.15535964969234, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0]"
        )
        self.expect_dfs(v1, [v.value for v in CfState.all_states()])
        p1 = json.loads(
            "[[0.5, 0, 0.5, 0], [0, 0, 1.0, 0], [0, 0, 1.0, 0], [0, 0, 1.0, 0], [0, 0, 1.0, 0], [0, 0, 0, 1.0], [0, 0, 0, 1.0], [0, 0, 0, 1.0], [0, 0, 0, 1.0], [0, 0, 0, 1.0], [0, 0, 0, 1.0], [0.5, 0, 0, 0.5], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [0, 0, 0, 1.0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [1.0, 0, 0, 0], [0, 0, 0, 1.0], [0, 1.0, 0, 0], [1.0, 0, 0, 0], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25]]"
        )
        self.expect_dfs(
            p1, [[a.p for a in v.get_actions().values()] for v in CfState.all_states()]
        )
        # logger.draw_line("record", diff_records)

    def test_ban(self):
        bs = Bandit()
        for cls in [EpsilonGreedy, DecayingEpsilonGreedy, Ucb, ThompsonSampling]:
            c: EpsilonGreedy = cls()
            c.load().run(bs)
            self.expect_array(bs.probs, c.estimates)
            logger.draw_line(f"{cls.__name__}", c.regret_record)


if __name__ == "__main__":
    random_seed(0)
    TestLn().run()
