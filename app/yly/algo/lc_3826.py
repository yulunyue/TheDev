from common.util.export import List, MockCf, functools, CT


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[1, 1, 1], k=3, result=3),
            case1=dict(nums=[1, 1, 1], k=2, result=4),
            case2=dict(nums=[5, 1, 2, 1], k=2, result=25),
        )

    def minPartitionScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        s = [0]
        if n == k:
            return sum([v * (v + 1) // 2 for v in nums])
        for v in nums:
            s.append(s[-1] + v)

        @functools.lru_cache(None)
        def dfs(i, k):
            if k == 1:
                v = s[-1] - s[i]
                return v * v
            ans = CT.inf
            for j in range(i + 1, n + 1 - k):
                v = s[j] - s[i]
                a = v * v + dfs(j, k - 1)
                if a < ans:
                    ans = a
            return ans

        return (dfs(0, k) + s[-1]) // 2

    execute = minPartitionScore
