from typing import List, Dict
from collections import defaultdict


class UniFind:
    def __init__(self) -> None:
        self.p = dict()
        

    def merge(self, parent, child):
        parent1 = self.find(parent)
        child1 = self.find(child)
        if parent1 == child1:
            return parent1, False
        self.p[child1] = parent1
        self.union(child,child1,parent,parent1)
        return parent1, True
    def union(self,ca,cb,pa,pb):
        pass
    def find(self, v):
        if v not in self.p:
            self.p[v] = v
            self.size[v] = 0
        if self.p[v] != v:
            p = self.find(self.p[v])  # 带路径权需要先更新 self.dis[self.p[v]]
            self.dis[v] += self.dis[self.p[v]]
            self.p[v] = p
        return self.p[v]

    def show(self):
        mp = defaultdict(list)
        for k in self.p.keys():
            if k == self.find(k):
                continue
            mp[self.find(k)].append(f"{k}: dis={self.dis[k]}")
        ret = []
        for k, value in mp.items():
            ret.append(f"---{k}: dis={self.dis[k]}---")
            ret.extend(value)
            ret.append("-------")
        return "\n".join(ret)
