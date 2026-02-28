from common.util.export import math


class Block:
    def __init__(self, size):
        self.n = math.ceil(math.sqrt(size))
        self.m = math.ceil(size / self.n)
        self.size = size
        self.data = [0] * size
        self.todo = [0] * self.m

    def get_l(self, idx):
        i = idx // self.n
        r = (i + 1) * self.n
        if r >= self.size:
            r = self.size
        return i, r - 1

    def get_r(self, idx):
        i = idx // self.n
        return i, i * self.n

    def set_data(self, idx, i, v):
        self.data[i] = v

    def update_area(self, i, l, r, v):
        if l % self.n == 0 and (r == self.size - 1 or r - l == self.n - 1):
            self.do(i, v)
            return
        self.set_datas(i, l, r, v)

    def set_datas(self, i, l, r, v):
        for j in range(l, r + 1):
            self.set_data(i, j, self.data[j] + v)
        self.down(i)

    def do(self, i, v):
        self.todo[i] += v
        return self

    def get(self, i):
        return self.data[i] + self.todo[i // self.n]

    def query_data(self, l, r):
        return sum(self.data[l : r + 1])

    def query_area(self, l, r, i):
        return self.query_data(l, r) + self.query_todo(i)

    def query_todo(self, i):
        if i == self.n - 1:
            return self.todo[i] * (self.size - i * self.n)
        return self.todo[i] * self.n

    def down(self, i):
        if self.todo[i] == 0:
            return
        for j in range(self.n):
            idx = j + i * self.n
            if idx >= self.size:
                break
            self.set_data(i, idx, self.data[idx] + self.todo[i])
        self.todo[i] = 0

    def update(self, l, r, v):
        il, lr = self.get_l(l)
        ir, rl = self.get_r(r)
        if il == ir:
            self.update_area(il, l, r, v)
        else:
            self.update_area(il, l, lr, v)
            self.update_area(ir, rl, r, v)
        while il + 1 <= ir - 1:
            self.do(il, v)
            il += 1

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
