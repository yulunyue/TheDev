from common.util.export import TestBase
from common.algo.base.block import isqrt2, Block


class TestBlock(TestBase):
    def test_isqrt(sefl):
        assert isqrt2(7) == (3, 3)

    def test_all(self):
        """
        0 1 2|3 4 5|6 7
        """
        b = Block(8)
        self.expect(b.n, 3)
        b.update(2, 5, 1)
        self.expect(b.data, [0, 0, 1, 0, 0, 0, 0, 0])
        self.expect(b.todo, [0, 1, 0])
        self.expect(b.query(0, 7), 4)
