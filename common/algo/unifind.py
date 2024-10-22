class UniFind:
    def __init__(self) -> None:
        self.p = dict()
        self.size = dict()

    def merge(self, f, t):
        f1 = self.find(f)
        t1 = self.find(t)
        if f1 == t1:
            return None
        self.p[f1] = t1
        self.size[t1] += self.size[f1]
        self.size[f1] = 0
        return t1

    def find(self, v):
        if v not in self.p:
            self.p[v] = v
            self.size[v] = 1
        if self.p[v] != v:
            self.p[v] = self.find(self.p[v])
        return self.p[v]

    def update(self):
        for k in self.p:
            self.find(k)

    def get_pkeys(self):
        return set(list(self.p.values()))
