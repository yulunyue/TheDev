from common.util.export import TestBase, logger
from app.yly.envs.ml.ciff_walk.player.sarse import SarseCf
from app.yly.envs.ml.ciff_walk.env import CfState, C


class TestQl(TestBase):
    def test_train(self):
        al = SarseCf().load()
        s = CfState.new(C.INIT_SATTE)
        al.train(s)
        view = al.view()
        logger.info(view)
        self.expect(view, C.BEST_MAP)
