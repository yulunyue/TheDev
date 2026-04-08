from common.util.export import TestBase


class A:
    d = dict()


class B(A):
    d = dict()


class TestPy:
    def test_eval(self):
        assert eval("1+1") == 2

    def test_zip(self):
        assert list(zip("12", "34")) == [("1", "3"), ("2", "4")]
