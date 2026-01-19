from common.util.export import TestBase, logger
from app.yly.envs.ml.ciff_walk.player.value_func import VFunc
from app.yly.envs.ml.ciff_walk.env import CfState, C


class TestQl(TestBase):
    def test_train(self):
        al = VFunc().load(train_epoll=100)
        s = CfState.new(C.INIT_SATTE)
        al.train(s)
        self.expect(al.view(), C.BEST_MAP)
