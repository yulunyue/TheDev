class XorBais:
    def set_length(self, n):
        self.n = n
        self.b = [0] * n
        return self

    def set_b(self, xs):
        self.set_length(max(xs).bit_length())
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

    def __repr__(self):
        return "\n".join(["----"] + [self.f(v) for v in self.b] + ["----"])

    def f(self, v):
        return format(v, f"0{self.n}b")
