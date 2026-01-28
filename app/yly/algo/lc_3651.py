from common.util.export import MockCf, List, defaultdict, heapq


class Solution:
    def get_cases(self):
        return dict(
            case0=dict(grid=[[1, 3, 3], [2, 5, 4], [4, 3, 5]], k=2, result=7),
        )

    def minCost(self, grid: List[List[int]], k: int) -> int:
        n, m = len(grid), len(grid[0])
        g = []
        for i in range(n):
            for j in range(m):
                u = grid[i][j]
                g.append([u, i, j])
        g.sort()
        ct = dict()
        for i, (v, _, _) in enumerate(g):
            ct[v] = i
        h = [(0, -k, 0, 0)]
        c = defaultdict(lambda: [float("inf"), 0])
        c[0, 0] = [0, -k]

        def add(i, j, co):
            if co[0] < c[i, j][0] or co[1] < c[i, j][1]:
                c[i, j] = co
                heapq.heappush(h, [co[0], co[1], i, j])

        while h:
            co, m, i, j = heapq.heappop(h)
            # print(co,i,j,m)
            if i == n - 1 and j == z - 1:
                return co
            u = grid[i][j]
            if m < 0:
                for l in range(ct[u] + 1):
                    v, y, x = g[l]
                    add(y, x, [co, m + 1])
            if i + 1 < n:
                add(i + 1, j, [co + grid[i + 1][j], m])
            if j + 1 < z:
                add(i, j + 1, [co + grid[i][j + 1], m])
