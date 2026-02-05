from common.util.export import List, MockCf, functools, CT, bisect


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[1, 1, 1], k=3, result=3),
            case1=dict(nums=[1, 1, 1], k=2, result=4),
            case2=dict(nums=[13, 8, 19], k=2, result=421),
            case3=dict(nums=[5, 1, 2, 1], k=2, result=25),
            case4=dict(nums=[18, 16, 50], k=2, result=25),
            case5=dict(nums=[17, 2, 43, 11, 44], k=4, result=0),
        )

    def minPartitionScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        s = [0]

        for v in nums:
            s.append(s[-1] + v)
        # self.logger.info(s)

        @functools.lru_cache(None)
        def dfs(i, k):
            if i + k == n:
                return sum(v * v for v in nums[i:])
            v = s[-1] - s[i]
            if k == 1:
                return v * v
            c = v / k
            j = i + 1

            u = s[j] - s[i]
            while u < c and j < n - k + 1:
                j += 1
                u = s[j] - s[i]
            # self.logger.map(i=i, j=j, k=k, v=v, c=c)
            a = u * u + dfs(j, k - 1)
            return a

        return (dfs(0, k) + s[-1]) // 2

    execute = minPartitionScore
