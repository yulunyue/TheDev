from common.util.export import TestBase, logger
from common.algo.export import MctsEasy, PolicyIteration, ValueIteration
from .model.mrp_state import computer, MrpState
from .model.mdp_state import MdpState, get_mrp_form_mdp
from .model.constant import C1, C2
import random


class TestMain(TestBase):
    """python -m app.yly.envs.ml.mrcf.test debug"""

    def test_mrp(self):
        s = MrpState.new(0)
        actions = s.get_steps([1, 2, 5])
        self.expect(s.get_seq_score_backward(actions, 0.5), -2.5)
        self.expect_ndarray(
            [
                MrpState.new(i).get_bellman_score(0.5)
                for i in range(len(C1.STATE_VALUE))
            ],
            C1.STATE_VALUE,
            2.2,
        )
        self.expect_ndarray(computer(C1.MRP_REWARD, C1.MRP_P), C1.STATE_VALUE)

    def test_mdp(self):
        rewards = [MdpState.new(i).get_pi_reawrd(C2.Pi_1) for i in range(1, 6)]
        self.expect_ndarray(rewards, C2.MDR_REWARDS)
        pi = get_mrp_form_mdp(C2.Pi_1)
        self.expect_ndarray(pi, C2.P_from_mdp_to_mrp)
        self.expect_ndarray(
            computer(C2.MDR_REWARDS, C2.P_from_mdp_to_mrp), C2.MDP_STATE
        )
        self.expect_ndarray(computer(rewards, pi), C2.MDP_STATE)

    def test_mct(self):
        m = MctsEasy().load(num_episodes=10000)
        m.train(MdpState.new(1))
        rewards = [
            m.mct_reward[MdpState.new(i + 1).state] for i in range(len(C2.MDP_STATE))
        ]
        self.expect_ndarray(rewards, C2.MDP_STATE, wucha=0.3)

    def test_mct1(self):
        m = MctsEasy().load(num_episodes=10000)
        m.train(MrpState.new(2))
        rewards = [m.mct_reward[i] for i in range(len(C1.STATE_VALUE))]
        self.expect_ndarray(rewards, C1.STATE_VALUE, wucha=1)

    def run_value(self):
        ValueIteration().load().train(MdpState)

    def run_policy(self):
        PolicyIteration().load().train(MdpState)

    def debug(self):
        self.test_mct1()


if __name__ == "__main__":
    TestMain().run()
