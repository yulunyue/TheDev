from common.util.export import logger, TestBase
from common.algo.export import ALgoManage, Algo
from .env import Flvo
from .model.constant import C
from .algo.qlearn import LkQl


class TestFlv(TestBase):
    def test_dev(self):
        LkQl().load().search(Flvo.new())

    def test_debug(self):
        self.test_dev()
