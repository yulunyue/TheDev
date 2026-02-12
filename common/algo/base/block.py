from common.util.export import math


class Block:
    def __init__(self, size):
        self.n = math.ceil(math.sqrt(size))
        self.size = size
        self.data = [0] * size
        self.todo = [0] * self.n

    def get_l(self, idx):
        i = idx // self.n
        l = i * self.n
        return i, min(l + self.n, self.size) - 1

    def get_r(self, idx):
        i = idx // self.n
        return i, i * self.n

    def update_area(self, l, r, v):
        if l + self.n - 1 == r:
            self.do(l // self.n, v)
            return
        for i in range(l, r + 1):
            self.data[i] += v

    def do(self, i, v):
        self.todo[i] = v
        return self

    def update(self, l, r, v):
        il, lr = self.get_l(l)
        ir, rl = self.get_r(r)
        if il == ir:
            self.update_area(l, r, v)
        else:
            self.update_area(l, lr, v)
            self.update_area(rl, r, v)
        while il + 1 <= ir - 1:
            self.do(il, v)
            il += 1

    def query_area(self, l, r, i):
        return sum(self.data[l : r + 1]) + self.todo[i] * (r - l + 1)

    def query_todo(self, i):
        if i == self.n - 1:
            return self.todo[i] * (self.size - i * self.n)
        return self.todo[i] * self.n

    def query(self, l, r):
        il, lr = self.get_l(l)
        ir, rl = self.get_r(r)
        ans = 0
        if il == ir:
            ans += self.query_area(l, r, il)
        else:
            ans += self.query_area(l, lr, il)
            ans += self.query_area(rl, r, ir)
        while il + 1 <= ir - 1:
            ans += self.query_todo(il + 1)
            il += 1
        return ans

    def down(self):
        for i, v in enumerate(self.todo):
            if v:
                for j in range(self.n):
                    self.data[j + i * self.n] += v
                self.todo[i] = 0
