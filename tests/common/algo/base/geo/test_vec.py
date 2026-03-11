from common.algo.base.geo.vec import Vec
from common.util.export import TestBase


class TestVec(TestBase):
    def test_base(self):
        a = Vec(2, 2)
        self.expect(a.is_left(Vec(2, 3)), True)
        self.expect(a.is_left(Vec(3, 3)), True)
        self.expect(a.is_right(Vec(3, 3)), True)
        self.expect(a.is_right(Vec(-2, -2)), True)
        self.expect(a.is_right(Vec(2, 1)), True)
