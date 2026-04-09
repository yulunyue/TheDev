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
        if k > n // 2:
            return -1
        ops = [0] * n
        for i in range(n):
            ops[i] = CT.max(0, 1 + CT.max(nums[i - 1], nums[(i + 1) % n]) - nums[i])
        self.log(ops=ops)

        @functools.lru_cache(None)
        def dfs(i, k, zero_has):
            if k == 0:
                return 0
            if i == n - 1 and zero_has:
                return dfs(i + 1, k, zero_has)
            if i >= n:
                return CT.inf
            c = ops[i] + dfs(i + 2, k - 1, zero_has or i == 0)
            b = dfs(i + 1, k, zero_has)
            # self.log(i=i, k=k, zero_has=zero_has, c=c, b=b)
            return CT.min(c, b)

        return dfs(0, k, False)

    execute = minOperations
