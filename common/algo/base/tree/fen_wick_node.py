class FenWickTree:
    """
                       16
           8
       4        12            20
     2   6   10    14     18
    1 3 5 7 9 11 13  15 17  19  21
    """

    def set_range(self, size, default_value=0):
        self.size = size
        self.array = [default_value] * size
        return self

    def update(self, i, v):
        while i < self.size:
            self.array[i] = self.calc(self.array[i], v)
            i += i & -i

    def query_one(self, i):
        if i <= 0:
            return 0
        ret = 0
        while i > 0:
            ret = self.calc(ret, self.array[i])
            i &= i - 1
        return ret

    def query(self, l, r):
        return self.query_one(r) - self.query_one(l - 1)

    def calc(self, a, b):
        return a + b
