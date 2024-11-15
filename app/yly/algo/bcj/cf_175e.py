

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq




try:
    from app.yly.algo.manage import SolutionBase

except:
    class SolutionBase:
        def input(self):
            return input()

        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass
        
        def exec(self):
            pass

        def run(self):
            print(self.exec())

inf = float("inf")
M = (10**9)+7


class UniFind:
    def __init__(self, n) -> None:
        self.p = [-1]*n
        # self.size = defaultdict(int)
        self.value = [0]*n

    def merge(self, parent, child, val=0):
        parent1, pval = self.find(parent)
        child1, cval = self.find(child)
        val += pval-cval
        self.value[child] = val
        if parent1 == child1:
            return parent1, False
        self.p[parent1] += self.p[child1]
        self.p[child1] = parent1
        return parent1, True

    def find(self, idx):
        idz = idy = idx
        value = 0
        while self.p[idx] >= 0:
            value += self.value[idx]
            idx = self.p[idx]
        while idy != idx:
            self.value[idy], value = value, value-self.value[idy]
            self.p[idy], idy = idx, self.p[idy]
        return idy, self.value[idz]

    def update(self):
        for k in self.p:
            self.find(k)

    def get_pkeys(self):
        return set(list(self.p.values()))


CASE1 ='''
6
0
0
1 2 1
2 1 5 2 2
1 1 2
1 3 4
30
'''
class Solution(SolutionBase):
    uri = "https://codeforces.com/contest/175/problem/E"
    gameinfo = ('cf',175,'E')

    def get_cases(self):
        return [CASE1]

    def exec(self):
        ans = 0
        n=int(self.input())
        uf = UniFind(self.n+1)
        for pid in range(1,n+1):
            ids = self.input().split(' ')
            for i in range(1,len(ids),2):
                cid, value = int(ids[i]), int(ids[i+1])
                parent, val = uf.find(cid)
                val += value
                ans += val
                uf.merge(pid, parent, val)
        return ans % M

if __name__ == '__main__':
    Solution().run()
