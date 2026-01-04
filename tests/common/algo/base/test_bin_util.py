from common.algo.base.bin_util import low_bits, ss_or_dp
from common.util.export import TestBase


class TestBinUtil(TestBase):
    def test_low_bits(self):
        self.expect(low_bits(0b101), [1, 4])

    def test_ss_or_bit(self):
        self.expect(ss_or_dp([1, 1]), [0, 2])
