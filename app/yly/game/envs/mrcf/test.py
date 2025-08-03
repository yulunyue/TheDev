from common.util.export import TestBase, logger
from .util import MdpAlgo
from .model.mrp_state import MarkovRewardProcess, C, computer
from .model.mdp_state import MarkovDecisionProcess


class TestMain(TestBase):
    def test_mrp(self):
        s = MarkovRewardProcess()
        self.expect(s.get_actions_score([0, 1, 2, 5]), -2.5)
        self.expect_ndarray(computer(C.MRP_REWARD, C.MRP_P), C.STATE_VALUE)
        self.expect_ndarray(s.berman(C.STATE_VALUE), C.STATE_VALUE)

    def test_mdp(self):
        s = MarkovDecisionProcess()
        pi = s.get_mrp_form_mdp(C.Pi_1)
        self.expect_ndarray(p, C.P_from_mdp_to_mrp)
        rewards = s.get_reawrd(C.Pi_1)
        self.expect_ndarray(rewards, C.MDR_REWARDS)
        self.expect_ndarray(computer(rewards, pi), C.MDP_STATE)

    def test_all(self):
        self.test_mdp()
        self.test_mrp()


if __name__ == "__main__":
    TestMain().run()
