from typing import List, Dict
from collections import defaultdict


class UniFind:
    def __init__(self) -> None:
        self.p = dict()
        self.size = defaultdict(int)
        self.value = defaultdict(int)
        self.init()

    def init(self):
        pass

    def set_values(self, vals):
        for i, v in enumerate(vals):
            self.value[i] = v
        return self

    def merge(self, parent, child):
        parent1 = self.find(parent)
        child1 = self.find(child)
        if parent1 == child1:
            return parent1, False
        self.p[child1] = parent1
        self.size[parent1] += self.size[child1] + 1
        self.size[child1] = 0
        return parent1, True

    def find(self, v):
        if v not in self.p:
            self.p[v] = v
            self.size[v] = 0
        if self.p[v] != v:
            self.p[v] = self.find(self.p[v])
        return self.p[v]

    def update(self):
        for k in self.p:
            self.find(k)

    def get_pkeys(self):
        return set(list(self.p.values()))

    def __str__(self):
        return f"{self.p}"
