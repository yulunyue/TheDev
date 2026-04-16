from common.util.export import List, MockCf, CT, defaultdict
from common.algo.base.math_util import prime_gcds

PG = prime_gcds(CT.MX)


class Solution(MockCf):
    """
    对于
    """

    def get_cases(self):
        return dict(
            case0=dict(nums=[4, 8, 12, 16], p=2, queries=[[0, 3], [2, 6]], result=1)
        )

    def countGoodSubseq(self, nums: list[int], p: int, queries: list[list[int]]) -> int:
        ct = defaultdict(int)
        self.n = 0

        def c(v, t):
            if v % p:
                return
            v = v // p
            for u in PG[v]:
                ct[u] += t
            self.n += t

        for v in nums:
            c(v, 1)
        self.log(n=self.n, ct=dict(ct))
        for j, (i, v) in enumerate(queries):
            c(v, 1)
            c(nums[i], -1)
            self.log(n=self.n, ct=dict(ct))
            nums[i] = v
            if max(ct.values()) < self.n:
                return j

    execute = countGoodSubseq
