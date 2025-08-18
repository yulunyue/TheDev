from common.util.export import logger, TestBase
from common.algo.export import ALgoManage, Algo
from .env import Flvo
from .model.constant import C
from .algo.qlearn import LkQl


class TestFlv(TestBase):
    def prepare(self, args=None):
        self.s = Flvo.new()

    def dev(self):
        # l = LkQl().load()
        # l.search(Flvo())
        logger.info(self.s)

    def debug(self):
        self.dev()


if __name__ == "__main__":
    TestFlv().dev()
