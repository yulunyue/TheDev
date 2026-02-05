from common.util.export import List, MockCf, functools, CT


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[1, 1, 1], k=3, result=3),
            case1=dict(nums=[1, 1, 1], k=2, result=4),
            case2=dict(nums=[13, 8, 19], k=2, result=421),
            case3=dict(nums=[5, 1, 2, 1], k=2, result=25),
        )

    def minPartitionScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        s = [0]

        for v in nums:
            s.append(s[-1] + v)

        @functools.lru_cache(None)
        def dfs(i, k):
            if k == 1:
                v = s[-1] - s[i]
                return v * v
            if i + k == n:
                return sum(v * v for v in nums[i:])
            ans = CT.inf
            for j in range(i + 1, n - k + 2):
                v = s[j] - s[i]
                a = v * v + dfs(j, k - 1)
                self.logger.map(i=i, j=j, k=k, a=a)
                if a < ans:
                    ans = a
            return ans

        return (dfs(0, k) + s[-1]) // 2

    execute = minPartitionScore
