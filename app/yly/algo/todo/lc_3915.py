from common.util.export import MockCf, functools, CT, List


class Solution(MockCf):
    """
    给定长度为n的数组nums，和k
    我们需要从nums选择一个子序列 s
    满足
        s[i+1]-s[i]>=k
        nums[s[i]],nums[s[i+1]] 交替增减
    求nums[s]的最大值

    对于 s[i]属于 [n-k,n) 最大值dadd[i],dsub[i]为 s[i]
    对于 s[i]属于 [n-k*2,n-k) 最大值为
        减,dadd[i] = s[i]+max(nums[i+k:] if v>s[i])
        加,dsub[i] = s[i]+max(nums[i+k:] if v<s[i])
    对于 s[i]属于 [n-k*3,n-2*k)
        减,s[i]+max(nums[i+k:] if v>s[i],dsub[i])
    """

    def get_cases(self):
        return dict(
            case0=dict(nums=[5, 4, 2], k=2, expected=7),
        )

    def maxAlternatingSum(self, nums: list[int], k: int) -> int:
        n = len(nums)

        @functools.lru_cache(None)
        def dfs(i, lc):
            mn = -CT.inf
            for j in range(i + k, n):
                c = nums[j] - nums[i]
                if c == 0 or c * lc > 0:
                    continue
                v = dfs(j, 1 if c > 0 else -1)
                if v > mn:
                    mn = v
            if mn == -CT.inf:
                mn = 0
            mn += nums[i]
            self.log(i=i, lc=lc, mn=mn)
            return mn

        ans = max(dfs(i, 0) for i in range(n))
        dfs.cache_clear()
        return ans

    execute = maxAlternatingSum
