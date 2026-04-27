from common.util.export import List, defaultdict, MockCf, Dict


class Solution(MockCf):
    def get_cases(self) -> Dict:
        return dict(
            case0=dict(grid=[[1, 1, 2]], expected=False),
        )

    def hasValidPath(self, grid: List[List[int]]) -> bool:
        n, m = len(grid), len(grid[0])
        g = defaultdict(list)
        drs = [
            [],
            [0, -1, {4, 6}, 0, 1, {3, 5}],
            [-1, 0, {3, 4}, 1, 0, {5, 6}],
            [0, -1, {1, 4, 6}, 1, 0, {2, 5}],
            [1, 0, {2, 5, 6}, 0, 1, {1, 3, 5}],
            [-1, 0, {2, 3, 4}, 0, -1, {1, 4, 6}],
            [-1, 0, {2, 3, 4}, 0, 1, {1, 3, 5}],
        ]
        for i, row in enumerate(grid):
            for j, v in enumerate(row):
                dr = drs[v]
                for k in range(0, 6, 3):
                    y, x = i + dr[k], j + dr[k + 1]
                    if y < 0 or x < 0 or y >= n or x >= m:
                        continue
                    if v not in dr[k + 2]:
                        continue
                    g[i, j].append((y, x))
        q = [(0, 0)]
        vt = {(0, 0)}
        while q:
            q, h = [], q
            for d in h:
                for nxt in g[d]:
                    if nxt in vt:
                        continue
                    if nxt[0] == n - 1 and nxt[1] == m - 1:
                        return True
                    vt.add(nxt)
                    q.append(nxt)
        return False

    execute = hasValidPath
