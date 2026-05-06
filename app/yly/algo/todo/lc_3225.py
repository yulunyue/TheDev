from common.util.export import MockCf, List, functools


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
                result=11,
            )
        )

    def maximumScore(self, grid: List[List[int]]) -> int:
        self.n, self.m = len(grid), len(grid[0])

        @functools.lru_cache(None)
        def dfs(i, j):
            pass

    execute = maximumScore
