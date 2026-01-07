from common.algo.base.bin_util import low_bits, ss_or_dp, low_high_dp
from common.util.export import TestBase, random


class TestBinUtil(TestBase):
    def test_low_bits(self):
        self.expect(low_bits(0b101), [1, 4])

    def test_ss_or_bit(self):
        self.expect(ss_or_dp([1, 1]), [0, 2])

    def test_low_high_dp(self):
        # 数位和被三整除
        def calc_args(v, a, i):
            return [(v + a) % 3]

        def ret_fun(a, i):
            return a == 0

        for _ in range(50):
            l, r = random.randint(3, 100), random.randint(105, 300)
            self.expect(
                low_high_dp(
                    l,
                    r,
                    0,
                    calc_args=calc_args,
                    ret_fun=ret_fun,
                ),
                r // 3 - (l - 1) // 3,
            )
