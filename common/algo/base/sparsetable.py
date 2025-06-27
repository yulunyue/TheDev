import functools
from typing import List


class SparseTable:
    """ """

    def load(self, a):
        self.n = len(a)
        self.m = self.n.bit_length()
        self.st = [a]
        return self

    def make_max(self):
        for j in range(1, self.m):
            k = self.n - (1 << j)
            tmp = [0] * self.n
            for i in range(k + 1):
                u = i + (1 << (j - 1))
                tmp[i] = max(self.st[j - 1][i], self.st[j - 1][u])
            self.st.append(tmp)
        return self

    def make_jump(self):
        for j in range(1, self.m):
            tmp = []
            for i in range(self.n):
                p = self.st[j - 1][i]
                tmp.append(self.st[j - 1][p])
            self.st.append(tmp)
        return self

    def query_jump(self, l, r):
        res = 0
        for k in range(self.m - 1, -1, -1):
            if self.st[k][r] > l:
                res |= 1 << k
                r = self.st[k][r]
        return res, r

    def query_max(self, l: int, r: int):
        if l >= r:
            return 0
        k = (r - l).bit_length() - 1
        r = r - (1 << k)
        return max(self.st[k][l], self.st[k][r])

    def __repr__(self):
        return "\n".join([str(v) for v in self.st])
