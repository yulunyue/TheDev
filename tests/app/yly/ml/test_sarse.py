from common.util.export import TestBase, logger
from common.algo.export import random_seed
from app.yly.envs.ml.ciff_walk.player.sarse import SarseCf
from app.yly.envs.ml.ciff_walk.env import CfState, C


class TestSarse(TestBase):
    def test_train(self):
        random_seed(0)
        al = SarseCf().load()
        s = CfState.new(C.INIT_SATTE)
        al.train(s)
        view = al.view()
        logger.info(view)
        self.expect(view.split("\n")[-3:], C.BEST_MAP.split("\n")[-3:], view)
