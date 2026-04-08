from common.util.export import TestBase
from common.algo.base.gaussian_elimination import GaussElimination


class TestGaussElimination(TestBase):
    def test_init(self):
        g = GaussElimination([1, 3, 4, 8, 9, 9], 5)
        self.expect(g.b, 5)
        self.expect(g.n, 6)
