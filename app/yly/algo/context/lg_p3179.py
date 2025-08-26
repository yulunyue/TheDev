from common.util.export import defaultdict, math, functools, logger, deepcopy
from common.mock import MockCf


class Solution(MockCf):
    uri = """https://www.luogu.com.cn/problem/P3179#ide"""

    def get_cases(self):
        return [dict(n=3, nums=[1, 2], result="Yes.")]

    def init(self):
        self.z = []
        self.mex = defaultdict(int)
        self.s = defaultdict(lambda: [0, 0])

    def exec_main(self, n, nums):
        self.pre_hander(n)
        y = 0
        for v in nums:
            y ^= self.sg(v)
        return "No" if y == 0 else "Yes"

    def main(self):
        n = self.ii()[0]
        for _ in range(self.ii()[0]):
            self.output(self.calc(n, self.ii()))

    def sg(self, x):
        if x > self.sqrt_n:
            return self.s[self.n // x][0]
        return self.s[x][1]

    def pre_hander(self, n):
        self.n = n
        self.sqrt_n = math.sqrt(n)
        self.z = [0]

        i = 1
        while i <= n:
            j = n // (n // i)
            self.z.append(j)
            i = j + 1
        # logger.map(z=z)
        for t in range(len(self.z) - 1, 0, -1):
            yh = 0
            self.mex[yh] = t
            i = self.z[t] * 2
            while i <= n:
                j = n // (n // i) // self.z[t] * self.z[t]
                self.mex[yh ^ self.sg(i)] = t
                if ((j - i) // self.z[t] + 1) & 1:
                    yh ^= self.sg(i)
                i = j + self.z[t]
            ans = 0
            while self.mex[ans] == t:
                ans += 1

            if self.z[t] > self.sqrt_n:
                self.s[n // self.z[t]][0] = ans
            else:
                self.s[self.z[t]][1] = ans

    def to_json(self):
        return dict(
            z=deepcopy(self.z), mex=deepcopy(dict(self.mex)), s=deepcopy(dict(self.s))
        )

    def __str__(self):
        return f"{self.z}{self.mex}{self.s}"


if __name__ == "__main__":
    Solution().main()
