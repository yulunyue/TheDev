from common.util.export import MockCf, List, heapq, defaultdict, bisect
from common.algo.base.unifind import UniFind


class Uf(UniFind):

    def merge(self, parent, child):
        _, flag = super().merge(parent, child)
        if flag:
            return True
        return (self.dis[parent] + self.dis[child]) % 2 == 1


class Solution(MockCf):

    def dis(self, i, j):
        return abs(self.points[i][0] - self.points[j][0]) + abs(
            self.points[i][1] - self.points[j][1]
        )

    def get_sort(self, points: List[List[int]]):
        self.points = points
        self.n = len(points)

        h = []
        for i in range(self.n):
            for j in range(i + 1, self.n):
                h.append([self.dis(i, j), i, j])
        h.sort()
        return h

    def maxPartitionFactor(self, points: List[List[int]]) -> int:

        h = self.get_sort(points)
        uf = Uf()

        while h:
            v, i, j = h.pop(0)
            if not uf.merge(i, j):
                return v
        return 0

    def maxPartitionFactor(self, points: List[List[int]]) -> int:
        """
        二分答案+二分图
        """

        h = self.get_sort(points)

        def check(i):
            ans = h[i][0]
            colors = [0] * self.n

            def dfs(x, c):
                colors[x] = c
                for y in range(self.n):
                    if y == x or self.dis(x, y) > ans:
                        continue
                    if colors[y] == c or (colors[y] == 0 and not dfs(y, -c)):
                        return False
                return True

            for i, c in enumerate(colors):
                if c == 0 and not dfs(i, 1):
                    return True
            return False

        return bisect.bisect_left(range(0, len(h)), True, key=check)

    execute = maxPartitionFactor
