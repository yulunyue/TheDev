from common.algo.base.comb import Comb
from common.util.export import MockCf, bisect

MX = 52
CMS = Comb().load(mx=MX)


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case1=dict(n=4, k=2, result=9),
            case2=dict(n=1, k=2, result=3),
            case3=dict(n=3, k=1, result=4),
            case0=dict(n=5, k=2, result=10),
        )

    def nthSmallest(self, n: int, k: int) -> int:
        a = 0
        if k == 1:
            return 1 << (n - 1)

        def c(i, j, n):
            v = CMS.comb(i, j)
            return n <= v

        for j in range(k, 0, -1):
            m = bisect.bisect_right(
                range(j, MX),
                False,
                key=lambda i: c(i, j, n),
            )
            m += j - 1
            v = CMS.comb(m, j)
            # self.logger.map(j=j, m=m, v=v, n=n)
            n -= v
            a |= 1 << m
        return a

    execute = nthSmallest
