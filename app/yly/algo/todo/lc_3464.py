from common.util.export import List, functools, bisect, LOG


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:

        def u(pos):
            x, y = pos
            if y == 0 or x == side:
                return x + y
            if y == side:
                return side * 3 - x
            return side * 4 - y

        def dis(i, j):
            return abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])

        points.sort(key=u)
        n = len(points)
        LOG.map(points=[[v[0], v[1], dis(i, i - 1)] for i, v in enumerate(points)])

        def check(v):
            nxt = [[0, 0] for _ in range(n)]
            j = 1
            for i in range(n):
                while dis(i, j) < v:
                    if i == 0:
                        nxt[j][1] = nxt[j - 1][1] + 1
                    j = (j + 1) % n
                if nxt[i][0] == k - 1 and nxt[j][1] <= nxt[i][1] and nxt[j][0] == 0:
                    LOG.map(v=v, nxt=nxt, r=False)
                    return False
                nxt[j][0] = nxt[i][0] + 1
                nxt[j][1] = nxt[i][1]
            LOG.map(v=v, nxt=nxt, r=True)
            return True

        return bisect.bisect_right(range(1, (side * 4 // n) + 2), False, key=check)
