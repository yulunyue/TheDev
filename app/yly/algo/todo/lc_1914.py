from common.util.export import List, Dict, functools, CT, LOG


class Solution:
    def rotateGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        n, m = len(grid), len(grid[0])
        dr = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        y1, x1, y2, x2 = 0, 0, n - 1, m - 1
        ret = [[0] * m for _ in range(n)]

        while y1 < y2 and x1 < x2:
            dr_idx = 0
            y3, x3 = y1, x1
            ts = []
            mp = {(y1, x1), (y1, x2), (y2, x2), (y2, x1)}
            while dr_idx < 4:
                y3 += dr[dr_idx][0]
                x3 += dr[dr_idx][1]
                ts.append([y3, x3])
                if (y3, x3) in mp:
                    dr_idx += 1

            for i in range(len(ts)):
                y3, x3 = ts[i]
                y4, x4 = ts[(i + k) % len(ts)]
                ret[y4][x4] = grid[y3][x3]
            y1, x1, y2, x2 = y1 + 1, x1 + 1, y2 - 1, x2 - 1
        return ret
