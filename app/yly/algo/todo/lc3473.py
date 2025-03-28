from common.algo.manage import SolutionBase, functools, List, inf


class Solution(SolutionBase):
    uri = "https://leetcode.cn/contest/weekly-contest-439/problems/sum-of-k-subarrays-with-length-at-least-m/description/"

    def get_cases(self):
        return [dict(nums=[1, 2, -1, 3, 3, 4], k=2, m=2, result=13)]

    def execute(self, nums: List[int], k: int, m: int) -> int:
        f = [0]
        n = len(nums)
        for i in range(n):
            f.append(f[-1] + nums[i])

        @functools.lru_cache(None)
        def dfs(i, k):
            if k == 0:
                ans = 0
            elif i + k * m >= n:
                ans = -inf if i + k * m > n else f[n] - f[i]
            else:
                ans = dfs(i + 1, k)
                for j in range(i + m, n + 1):
                    ans = max(ans, f[j] - f[i] + dfs(j, k - 1))
            self.log(k, nums[i:], ans)
            return ans

        return dfs(0, k)

    def maxSum(self, *args, **kw):
        self.init(*args, **kw)
        return self.execute(*args, **kw)


if __name__ == "__main__":
    Solution().run()
