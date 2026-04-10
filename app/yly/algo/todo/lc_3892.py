from common.util.export import List, Dict, MockCf, CT, functools


class Solution(MockCf):
    """
    给定一个
    贪心策略
    对于任一个高峰的三个点，我们增加它没有意义

    """

    def get_cases(self):
        return dict(
            case0=dict(nums=[4, 2, 0, 1, 3], k=2, result=3),
            case1=dict(nums=[4, 5, 3, 6], k=2, result=0),
        )

    def minOperations(self, nums: list[int], k: int) -> int:
        n = len(nums)

        ops = [0] * n
        for i in range(n):
            ops[i] = CT.max(0, 1 + CT.max(nums[i - 1], nums[(i + 1) % n]) - nums[i])
        r = CT.min(self.op2(ops[: n - 1], k), self.op2(ops[1:n], k))
        return -1 if r == CT.inf else r

    def op2(self, ops, k):
        n = len(ops)
        self.log(ops=ops, k=k)

        @functools.lru_cache(None)
        def dfs(i, k):
            if i == 0:
                return ops[0]
            if i + 2 < k * 2:
                return CT.inf
            b = dfs(i - 1, k)
            if k == 1:
                return CT.min(ops[i], b)
            c = ops[i] + dfs(i - 2, k - 1)
            self.log(i=i, ops=ops, k=k)
            return CT.min(c, b)

        r = dfs(n - 1, k)
        dfs.cache_clear()
        return r

    execute = minOperations
