from common.util.export import logger, TestBase
from common.algo.export import ALgoManage, Algo
from .env import Flvo
from .model.constant import C
from .algo.qlearn import LkQl


class TestFlv(TestBase):
    def test_dev(self):
        l = LkQl().load()
        l.search(Flvo())
        l.draw()

    def test_debug(self):
        self.test_dev()
