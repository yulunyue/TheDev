from common.util.export import defaultdict, math, functools, logger
from common.mock import MockCf


@functools.lru_cache(None)
def pre_hander(n):
    mex = defaultdict(int)
    sqrt_n = math.sqrt(n)
    s = defaultdict(lambda: [0, 0])
    z = [0]

    def sg(x):
        if x > sqrt_n:
            return s[n // x][0]
        return s[x][1]

    i = 1
    while i <= n:
        j = n // (n // i)
        z.append(j)
        i = j + 1
    # logger.map(z=z)
    for t in range(len(z) - 1, 0, -1):
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

        if z[t] > sqrt_n:
            s[n // z[t]][0] = ans
        else:
            s[z[t]][1] = ans
    logger.map(z=z, mex=dict(mex), s=dict(s))
    return sg


class Solution(MockCf):
    uri = """https://www.luogu.com.cn/problem/P3179#ide"""

    def get_cases(self):
        return [dict(n=3, nums=[1, 2], result="Yes.")]

    def calc(self, n, nums):
        sg = pre_hander(n)
        y = 0
        for v in nums:
            y ^= sg(v)
        return "No" if y == 0 else "Yes"

    def main(self):
        n = self.ii()[0]
        for _ in range(self.ii()[0]):
            self.output(self.calc(n, self.ii()))


if __name__ == "__main__":
    Solution().main()
