from common.util.export import defaultdict, math
from common.mock import MockCf

s1 = """3
2
2
1 2
2
2 3"""

o1 = """Yes
No"""


class Solution(MockCf):
    uri = """https://www.luogu.com.cn/problem/P3179#ide"""

    def get_cases(self):
        return [[s1, o1]]

    def run(self):
        n, *args = self.ii()
        m, *args = self.ii()
        i, j = 1, 0
        idx = 0
        z = defaultdict(int)
        mex = defaultdict(int)
        s = defaultdict(lambda: [0, 0])

        def sg(x):
            if x > math.sqrt(n):
                return s[n / x][0]
            return s[x][1]

        while i <= n:
            j = n // (n // i)
            idx += 1
            z[idx] = j
            i = j + 1
        for t in range(idx, 0, -1):
            yh = 0
            mex[yh] = t
            i = z[t] * 2
            while i <= n:
                j = n // (n // i) // z[t] * z[t]
                mex[yh ^ sg(i)] = t
                if ((j - i) // z[t] + 1) & 1:
                    yh ^= sg(i)
                i = j + z[t]
            ans = 0
            while mex[ans] == t:
                ans += 1
            if z[t] > math.sqrt(n):
                s[n / z[t]][0] = ans
            else:
                s[n / z[t]][1] = ans
        result = []
        for _ in range(m):
            self.ii()
            y = 0
            for v in self.ii():
                y ^= sg(v)
            result.append("No" if y == 0 else "Yes")
        return "\n".join(result)


if __name__ == "__main__":
    Solution().run()
