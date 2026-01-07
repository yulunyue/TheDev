from common.util.export import List, MockCf
from common.algo.base.bin_util import low_high_dp


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(low=1, high=100, result=9),
        )

    def countBalanced(self, low: int, high: int) -> int:
        # 数位和被三整除
        def calc_args(v, a, i):
            return [a + (v if i % 2 == 0 else -v)]

        def ret_fun(a, i):
            return a == 0

        return low_high_dp(
            low,
            high,
            0,
            calc_args=calc_args,
            ret_fun=ret_fun,
        )

    execute = countBalanced


if __name__ == "__main__":
    Solution().run()
