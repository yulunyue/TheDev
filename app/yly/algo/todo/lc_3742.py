from common.util.export import List, MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(case0=dict(grid=[[0, 1], [2, 0]], k=1, expected=2))

    def maxPathScore(self, grid: List[List[int]], k: int) -> int:
        n, m = len(grid), len(grid[0])
        q = [[0, 0, {0: grid[0][0]}]]
        while q:
            q, h = [], q
            for y, x, a in h:
                if y == n - 1 and x == m - 1:
                    return max(a.values())
                uv = grid[y][x]
                for dy, dx in [[0, 1], [1, 0]]:
                    ny, nx = y + dy, x + dx
                    if ny >= n or nx >= m or nx < 0 or ny < 0:
                        continue
                    u = {}
                    uk = 1 if uv else 0
                    for ck, cv in a.items():
                        if uk + ck <= k:
                            u[uk + ck]
                    if u:
                        q.append([ny, nx, u])
        return -1

    execute = maxPathScore
