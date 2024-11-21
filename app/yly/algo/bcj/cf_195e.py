

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq




try:
    from app.yly.algo.manage import SolutionBase,div,bs,divh,divv,tree

except:
    class SolutionBase:
        def i1(self):
            return int(sys.stdin.readline().strip())
        def il(self,n):
            return [[int(v) for v in sys.stdin.readline().strip().split(' ')] for _ in range(n)]
        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass
        
        def exec(self):
            pass

        def run(self):
            print(self.exec())

inf = float("inf")
MOD = (10**9)+7


class UniFind:
    def __init__(self, n) -> None:
        self.p = [-1]*n
        self.value = [0]*n

    def merge(self, parent, child, val=0):
        parent1, pval = self.find(parent)
        child1, cval = self.find(child)
        val = val+pval-cval
        self.value[child] = val
        if parent1 == child1:
            return parent1, False
        self.p[parent1] = self.p[parent1]+self.p[child1]
        self.p[child1] = parent1
        return parent1, True

    def find(self, idx):
        idz = idy = idx
        value = 0
        while self.p[idx] >= 0:
            value = value+self.value[idx]
            idx = self.p[idx]
        while idy != idx:
            self.value[idy], value = value, value-self.value[idy]
            self.p[idy], idy = idx, self.p[idy]
        return idy, self.value[idz]



    def algo_view(self):
        root_child=[]
        nodes=[dict(title=f'{i}',childs=[]) for i,v in enumerate(self.p)]
        for i,v in enumerate(self.p):
            if v==i:
                root_child.append(nodes[i])
            else:
                nodes[v]['childs'].append(nodes[i])
        return dict(childs=root_child,title='root')

    def hex_str(self):
        return str(self.p) 


CASE1 ='''
6
0
0
1 2 1
2 1 5 2 2
1 1 2
1 3 4
'''
class Solution(SolutionBase):
    uri = "https://codeforces.com/contest/195/problem/E"
    gameinfo = ('cf',195,'E')
    has_view = True
    def get_cases(self):
        return [
            dict(input=CASE1,result=30),
        ]
    def init(self, **kwargs):
        self.n= self.i1()
        self.uf = UniFind(self.n+1)
        self.lines = self.il()

    def get_watch(self):
        return divv(
            div(),
            tree()
        )
    def exec(self,**kg):
        ans = 0
        for pid in range(1,self.n+1):
            ids = self.lines[i-1]
            for i in range(1,len(ids),2):
                cid, value = ids[i], ids[i+1]
                parent, val = self.uf.find(cid)
                val += value
                ans += val
                self.uf.merge(pid, parent, val)
        return ans % MOD
    
    def execute(self,*args,**kwargs):
        return self.exec()
    
if __name__ == '__main__':
    Solution().run()

