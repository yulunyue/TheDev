from typing import List, Dict
from collections import defaultdict


class UniFind:
    def __init__(self, n=None) -> None:
        if n is None:
            self.p = dict()
        else:
            self.p = list(range(0, n))
        self.size = 0

    def merge(self, child, parent, *args):
        parent_parant = self.find(parent)
        child_parant = self.find(child)
        if self.can_merge(child, child_parant, parent, parent_parant, *args):
            self.p[child_parant] = parent_parant
            self.size += 1
            return parent_parant, True
        return None, False

    def can_merge(self, child, child_parant, parent, parent_parant, *args):
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
        return child_parant != parent_parant

    def find(self, v):
        if isinstance(self.p, dict) and v not in self.p:
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
        if isinstance(self.p,list):
            datas=enumerate(self.p)
        else:
            datas=self.p.items()
        for k,v in datas:
            if k == self.find(k):
                continue
            mp[self.find(k)].add(k)
        ret = ["-" * 10]
        for k, value in mp.items():
            ret.append(f"{k}:{self.value[k]}")
            for v in value:
                ret.append(f"-{v}:{self.value[v]}")
        ret.append("-" * 10)
        return "\n".join(ret)
