from common.util.export import TestBase, logger
from app.yly.envs.ml.ciff_walk.player.ql import Ql
from app.yly.envs.ml.ciff_walk.env import CfState, C


class TestQl(TestBase):
    def test_train(self):
        al = Ql().load().set_train_epoll(1000)
        s = CfState.new(C.INIT_SATTE)
        al.train(s)
        view = al.view()
        logger.info(view)
        self.expect(view.split("\n")[-3:], C.BEST_MAP.split("\n")[-3:], view)
