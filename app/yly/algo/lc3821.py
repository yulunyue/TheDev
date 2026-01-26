from common.algo.base.comb import Comb
from common.util.export import MockCf, bisect

MX = 52
CMS = Comb().load(mx=MX)


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(n=4, k=2, result=9),
        )

    def nthSmallest(self, n: int, k: int) -> int:
        a = 0

        def c(i, j, n):
            return CMS.comb(i + 1, j) <= n

        for j in range(k, 0, -1):
            m = bisect.bisect_right(range(0, MX), False, lambda i: c(i, j, n)) - 1
            n -= CMS.comb(m + 1, k)
            a |= 1 << m
        return a

    execute = nthSmallest
