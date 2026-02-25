from common.util.export import TestBase


class TestPy(TestBase):
    def test_eval(self):
        self.expect(eval("1+1"), 2)
