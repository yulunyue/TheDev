from common.util.export import logger, heapq, defaultdict
from common.mock import MockCf

s0 = """2
2 9 11
2 11 13"""
o0 = """4
9 0
9 2
13 2
13 0"""
s1 = """5
3 -3 0
2 -1 1
4 2 4
2 3 7
3 6 8"""
o1 = """14
-3 0
-3 3
0 3
0 2
1 2
1 0
2 0
2 4
4 4
4 2
6 2
6 3
8 3
8 0"""

s2 = """8
7 4 9
2 9 11
2 11 13
1 -3 -2
4 4 8
4 0 3
6 2 7
3 5 6"""
o2 = """14
-3 0
-3 1
-2 1
-2 0
0 0
0 4
2 4
2 6
4 6
4 7
9 7
9 2
13 2
13 0"""


class Solution(MockCf):
    uri = """https://codeforces.com/problemset/problem/35/E"""

    def run(self):
        n, *args = self.ii()
        ans = []
        area = []
        ct = dict()
        for _ in range(n):
            y, l, r = self.ii()
            area.append([l, 0, y])
            area.append([r, 1, y])
        keys = sorted(area)
        hq = [0]
        ans = []
        for x, tp, y in keys:
            if tp == 0:
                if hq and y > -hq[0]:
                    ans.append(f"{x} {-hq[0]}")
                    ans.append(f"{x} {y}")
                heapq.heappush(hq, -y)
                ct[y] = ct.get(y, 0) + 1
            else:
                ct[y] -= 1
                if hq and -hq[0] == y and ct[y] == 0:
                    ans.append(f"{x} {y}")
                    while hq and ct.get(-hq[0]) == 0:
                        heapq.heappop(hq)
                    ans.append(f"{x} {-hq[0]}")
        return ans

    def get_cases(self):
        return [[s0, o0], [s1, o1], [s2, o2]]


if __name__ == "__main__":
    Solution().main()
