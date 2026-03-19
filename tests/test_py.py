from common.util.export import TestBase


class TestPy:
    def test_eval(self):
        assert eval("1+1"), 2
