from common.util.export import TestBase, logger
from app.yly.algo.cg.cw.main import CgCw


class CwTest(TestBase):
    def test_make(self):
        CgCw().compile_one()


if __name__ == "__main__":
    CwTest().run()
