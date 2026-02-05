from common.util.export import List, MockCf, functools, CT, bisect


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[1, 1, 1], k=3, result=3),
            case1=dict(nums=[1, 1, 1], k=2, result=4),
            case2=dict(nums=[13, 8, 19], k=2, result=421),
            case3=dict(nums=[5, 1, 2, 1], k=2, result=25),
            case4=dict(nums=[18, 16, 50], k=2, result=25),
        )

    def minPartitionScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        s = [0]

        for v in nums:
            s.append(s[-1] + v)

        @functools.lru_cache(None)
        def dfs(i, k):
            if i + k == n:
                return sum(v * v for v in nums[i:])
            v = s[-1] - s[i]
            if k == 1:
                return v * v
            c = v / k
            j = i + 1
            while j < n - k + 3:
                u = s[j] - s[i]
                if u >= c:
                    a1 = u * u + dfs(j, k - 1)
                    if u > c and j - 1 > i:
                        u2 = s[j - 1] - s[i]
                        a2 = u2 * u2 + dfs(j - 1, k - 1)
                        if a2 < a1:
                            a1 = a2
                    return a1
                j += 1
            raise Exception(i, j, k, v)
            # ans = CT.inf
            # for j in range(i + 1, n - k + 2):
            #     v = s[j] - s[i]
            #     a = v * v + dfs(j, k - 1)
            #     # self.logger.map(i=i, j=j, k=k, a=a)
            #     if a < ans:
            #         ans = a
            # return ans

        return (dfs(0, k) + s[-1]) // 2

    execute = minPartitionScore
