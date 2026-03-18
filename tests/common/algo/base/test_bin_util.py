from common.algo.export import low_bits, ss_or_dp, low_high_dp, set_mask
from common.util.export import TestBase, random


class TestBinUtil(TestBase):
    def test_low_bits(self):
        self.expect(low_bits(0b101), [1, 4])

    def test_ss_or_bit(self):
        self.expect(ss_or_dp([1, 1]), [0, 2])

    def test_low_high_dp(self):
        # 数位和被三整除
        def calc_args(v, a, depth):
            return [(v + a) % 3]

        def ret_fun(v, depth):
            return v == 0

        for _ in range(6):
            l, r = random.randint(3, 50), random.randint(105, 200)
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

    def test_setmask(self):
        self.expect(set_mask(0b11011, 1, 3, 0b100), 0b11001)
        self.expect(set_mask(0b11011, 1, 3, 0b11), 0b10111)
