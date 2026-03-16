from common.util.export import List, MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(
                grid=[
                    [3, 4, 5, 1, 3],
                    [3, 3, 4, 2, 3],
                    [20, 30, 200, 40, 10],
                    [1, 5, 5, 4, 1],
                    [4, 3, 2, 2, 5],
                ],
                result=[228, 216, 211],
            ),
            case1=dict(
                grid=[
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9],
                ],
                result=[20, 9, 8],
            ),
        )

    def getBiggestThree(self, grid: List[List[int]]) -> List[int]:
        n, m = len(grid), len(grid[0])
        nm = max(n, m)
        a = n + m
        s = [[], []]
        dr = [[1, 1], [-1, 1]]
        dt = {0: dict(), 1: dict()}
        for i in range(a - 1):
            y, x = [0, n - 1], [i, i]
            if i >= m:
                y[0], x[0] = i - m + 1, 0
                y[1], x[1] = i - m, 0
            for j, (dy, dx) in enumerate(dr):
                s[j].append([0])
                for k in range(nm):
                    ay, ax = y[j] + k * dy, x[j] + k * dx
                    if ay < 0 or ay >= n or ax < 0 or ax >= m:
                        continue
                    dt[j][ay, ax] = [i, len(s[j][-1])]
                    s[j][-1].append(s[j][-1][-1] + grid[ay][ax])

        def f(i, y1, x1, a1):
            i1, i2 = dt[i][y1, x1]
            return s[i][i1][i2 + a1] - s[i][i1][i2 - 1]

        def calc(y, x, l):
            if l == 0:
                return grid[y][x]
            ret = (
                f(0, y, x - l, l)
                + f(1, y, x - l, l)
                + f(0, y - l, x, l)
                + f(1, y + l, x, l)
                - grid[y][x - l]
                - grid[y][x + l]
                - grid[y - l][x]
                - grid[y + l][x]
            )
            # self.logger.map(y=y, x=x, l=l, r=ret)
            return ret

        mx = []
        for i in range(n):
            yt, yb = i, n - i - 1
            for j in range(m):
                xl, xr = j, m - j - 1
                l = min(xl, xr, yt, yb)
                mx.append(calc(i, j, l))
        # self.logger.info(mx)
        return sorted(mx, reverse=True)[:3]

    execute = getBiggestThree
