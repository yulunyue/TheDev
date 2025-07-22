from common.util.export import List, math, defaultdict, logger, C


class Solution:
    def get_cases(self):
        return [
            dict(points=[[-3, 2], [3, 0], [2, 3], [3, 2], [2, -3]], result=2),
            dict(
                points=[[34, 88], [-62, -38], [26, 88], [91, 88], [47, -38]], result=3
            ),
            dict(points=[[-32, 12], [-32, -94], [-32, -15], [-30, 88]], result=0),
            dict(
                points=[[34, 88], [-62, -38], [26, 88], [91, 88], [47, -38]], result=3
            ),
            dict(
                points=[
                    [71, -89],
                    [-75, -89],
                    [-9, 11],
                    [-24, -89],
                    [-51, -89],
                    [-77, -89],
                    [42, 11],
                ],
                result=10,
            ),
        ]

    def countTrapezoids(self, points: List[List[int]]) -> int:
        ct1 = defaultdict(lambda: defaultdict(int))
        ct2 = defaultdict(lambda: defaultdict(int))
        n = len(points)
        for i in range(1, n):
            for j in range(i):
                x, y = points[j][0] - points[i][0], points[j][1] - points[i][1]
                if x == 0:
                    k = C.inf
                    c = points[i][0]
                else:
                    k = y / x
                    c = (points[i][1] * x - y * points[i][0]) / x

                ct1[k][c] += 1
                ct2[points[j][0] + points[i][0], points[j][1] + points[i][1]][k] += 1

        def u(ct):
            ans = 0
            for m in ct.values():
                s = 0
                for c in m.values():
                    ans += s * c
                    s += c
            return ans

        # logger.map(c=dict(ct))
        return u(ct1) - u(ct2)
