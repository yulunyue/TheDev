from common.util.export import List, MockCf, defaultdict, CT


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(
                grid=[
                    [0, 1],
                    [2, 0],
                ],
                k=1,
                expected=2,
            ),
            case1=dict(grid=[[0, 1], [1, 2]], k=1, expected=-1),
        )

    def maxPathScore(self, grid: List[List[int]], k: int) -> int:
        n, m = len(grid), len(grid[0])
        dt = defaultdict(lambda: -CT.inf)
        dt[0, 0, 0] = 0
        for i in range(n):
            for j in range(m):
                v = grid[i][j]
                for k1 in range(1, k + 1):
                    k2 = k1 - 1 if v else k1
                    if i == 0 and j == 0:
                        dt[i, j, k1] = 0
                    elif i == 0:
                        dt[i, j, k1] = dt[i, j - 1, k2] + v
                    elif j == 0:
                        dt[i, j, k1] = dt[i - 1, j, k2] + v
                    else:
                        dt[i, j, k1] = max(dt[i - 1, j, k2], dt[i, j - 1, k2]) + v

        # self.log(dt=dict(dt))
        ans = dt[n - 1, m - 1, k]
        return -1 if ans == -CT.inf else ans

    execute = maxPathScore
