from common.util.export import List, logger, get_log


class XorBais:
    def set_length(self, n):
        self.n = n
        self.b = [0] * n
        return self

    def set_b(self, xs: List[int]):
        mx = max(xs)
        self.set_length(mx.bit_length())
        for b in xs:
            self.insert(b)
        return self

    def insert(self, x: int):
        while x:
            i = x.bit_length() - 1
            if self.b[i] == 0:
                self.b[i] = x
                return
            x ^= self.b[i]

    def max_xor(self):
        res = 0
        for i in range(self.n - 1, -1, -1):
            if res ^ self.b[i] > res:
                res ^= self.b[i]
        return res
