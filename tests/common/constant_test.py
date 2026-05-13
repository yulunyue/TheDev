from common.util.export import TestBase, logger
from common.constant import Constant, CT


class TestConstant(TestBase):
    def test_base(self):
        self.expect(CT.min(0, 1), 0)
