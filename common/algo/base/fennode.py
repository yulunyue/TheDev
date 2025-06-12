class FenNode(View):
    """
                       16
           8
       4        12            20
     2   6   10    14     18
    1 3 5 7 9 11 13  15 17  19  21
    """

    def set_range(self, size, default_value=0):
        self.size = size + 1
        self.array = [default_value] * (size + 1)
        return self

    def update(self, i, v):
        self.i = i + 1
        while self.i < self.size:
            self.array[self.i] = v(self.array[self.i])
            self.i += self.i & -self.i

    def add(self, i, v):
        return self.update(i, lambda a: a + v)

    def query_value(self, i, f):
        ret = 0
        self.i = i
        while self.i > 0:
            ret = f(ret, self.array[self.i])
            self.i &= self.i - 1
        return ret

    def query_sum(self, l):
        return self.query_value(l, lambda a, b: a + b)
