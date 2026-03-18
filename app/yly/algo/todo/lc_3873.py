from common.util.export import List, MockCf, defaultdict


class Solution(MockCf):
    def get_cases(self):
        return dict(case0=dict(points=[[1, 1], [1, 2], [2, 2]], result=4))

    def maxActivated(self, points: list[list[int]]) -> int:
        n = len(points)
        vt = [0] * n
        ans = []
        g = defaultdict(list)
        for i, (y, x) in enumerate(points):
            g[0, y].append(i)
            g[1, x].append(i)

        def dfs(idx):
            if vt[idx]:
                return 0
            vt[idx] = 1
            y, x = points[idx]
            for j in g[0, y] + g[1, x]:
                vt[idx] += dfs(j)
            return vt[idx]

        for i in range(n):
            if vt[i]:
                continue
            ans.append(dfs(i))

        if len(ans) == 1:
            return ans[0] + 1
        return sum(sorted(ans)[-2:]) + 1

    execute = maxActivated
