from typing import List, Dict
from collections import defaultdict


class UniFind:
    def __init__(self) -> None:
        self.p = dict()

    def merge(self, child, parent, *args):
        parent1 = self.find(parent)
        child1 = self.find(child)
        if self.can_merge(child, child1, parent, parent1, *args):
            self.p[child1] = parent1
            return parent1, True
        return None, False

    def can_merge(self, from_, x, to, y, *args):
        """
        乘法的带权并查集
        #    x      y
        #  /       /
        # from_   to
        x/from_ = self.value[from_]
        y/to = self.value[to]
        to/from_ = value
        y/x = (to/from_)*(y/to)/(x/form_)
        """
        return x == y

    def find(self, v):
        if v not in self.p:
            self.p[v] = v
        if self.p[v] != v:
            p = self.find(self.p[v])
            self.connect(v, self.p[v])
            self.p[v] = p
        return self.p[v]

    def connect(self, child, parent):
        pass

    def show(self):
        mp = defaultdict(set)
        for k in self.p.keys():
            if k == self.find(k):
                continue
            mp[self.find(k)].add(k)
        ret = ["-" * 10]
        for k, value in mp.items():
            ret.append(f"{k}:{value}")
        ret.append("-" * 10)
        return "\n".join(ret)
