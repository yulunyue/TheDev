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
    Qlearning,
)


class TestLn(TestBase):

    def test_cfsarsa(self):
        rewards = dict()
        for step in [1, 5]:
            for s in CfState.all_states():
                for a in s.get_actions().values():
                    a.set_value(0)
            s = Sarsa().load(num_episodes=50, n_step=int(step))
            rewards[step] = dict(y=[])
            for i in range(10):
                rewards[step]["y"] += s.run(CfState)
                logger.info(f"---{i}--- rewards:{np.mean(rewards[step]['y'][-10:])}")
            logger.info(CfState.to_str())
        logger.draw_line(f"cfsarsa", rewards)

    def test_cfql(self):
        q = Qlearning().load(num_episodes=500)
        logger.draw_line("cfql", q.run(CfState))
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
