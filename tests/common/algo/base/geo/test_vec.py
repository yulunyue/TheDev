from common.algo.base.geo.vec import Vec
from common.util.export import TestBase


class TestVec(TestBase):
    def test_base(self):
        a = Vec(2, 2)
        self.expect(a.on_the_right_of(Vec(2, 3)), True)
        self.expect(a.on_the_right_of(Vec(3, 3)), True)
        self.expect(a.on_the_left_of(Vec(3, 3)), True)
        self.expect(a.on_the_left_of(Vec(-2, -2)), True)
        self.expect(a.on_the_left_of(Vec(2, 1)), True)
