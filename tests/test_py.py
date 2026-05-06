from common.util.export import TestBase, math, bisect


class TestPy:
    def test_eval(self):
        assert eval("1+1") == 2

    def test_zip(self):
        assert list(zip("12", "34")) == [("1", "3"), ("2", "4")]

    def test_math(self):
        assert math.log(2, 2) == 1
        assert math.log(1, 2) == 0
        assert math.log(8, 2) == 3

    def test_bisect(self):
        assert bisect.bisect_left([2, 3, 4], 3) == 1
        assert bisect.bisect_left([2, 3, 4], True, key=lambda v: v == 3) == 1
