from common.util.export import TestBase, logger
from app.yly.envs.ml.ciff_walk.player.pi_func import PiFunc
from app.yly.envs.ml.ciff_walk.env import CfState, C


class TestPiFunc(TestBase):
    def test_train(self):
        al = PiFunc().load(train_epoll=100)
        s = CfState.new(C.INIT_SATTE)
        al.train(s)
        self.expect(al.view(), C.BEST_MAP)
        self.expect(C.ACS[al.search(s).action], "^")
