class XorBais:
    def __init__(self, n):
        self.n = n
        self.b = [0] * n

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
