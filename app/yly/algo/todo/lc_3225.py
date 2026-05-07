from common.util.export import MockCf, List, functools, CT


class Solution(MockCf):
    """
    给定一个m行n列的矩阵g，矩阵中的元素都>0，我们需要尽可能的选择其中的一些元素，使得和最大。
    选择的规则是，如果选择(i，j)，则对于两个集合
    g[0:i+1][j-1],g[0:i+1][j+1]
    我们必须放弃其中一个集合的元素

    可以使用动态规划
    f[i,j]=max(f[i-1,j],g[i,j]+f[i,j-1])
    """

    def get_cases(self):
        return dict(
            case0=dict(
                grid=[
                    [0, 0, 0, 0, 0],
                    [0, 0, 3, 0, 0],
                    [0, 1, 0, 0, 0],
                    [5, 0, 0, 3, 0],
                    [0, 0, 0, 0, 2],
                ],
                expected=11,
            )
        )

    def calc(self, j, cur, pre):
        return self.g[pre][j] - self.g[cur][j] if pre > cur else 0

    def maximumScore(self, grid: List[List[int]]) -> int:
        self.n, self.m = len(grid), len(grid[0])
        self.g = [[0] * self.m for _ in range(self.n + 1)]
        for j in range(self.m):
            for i in range(self.n):
                self.g[i + 1][j] = self.g[i][j] + grid[i][j]

        @functools.lru_cache(None)
        def dfs(j, cur, pre):
            if j == 0:
                return self.calc(j, cur, pre)
            ans = 0
            for nxt in range(self.n + 1):
                d = self.calc(j, cur, max(nxt, pre))
                ans = max(ans, d + dfs(j - 1, nxt, cur))
            return ans

        return max(dfs(self.m - 1, i, 0) for i in range(self.n + 1))

    execute = maximumScore
