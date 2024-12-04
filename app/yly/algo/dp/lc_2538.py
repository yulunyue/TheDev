from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from sortedcontainers import SortedList
from functools import lru_cache
import bisect
import sys
import math
import heapq
try:
    from app.yly.algo.manage import SolutionBase,div,divh,divv,tree
except:
    class SolutionBase:
        def log(self, *args, **kwargs):
            pass

        def run(self):
            pass
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7

class Graph:
    def __init__(self,env):
        self.env:Solution=env
        self.g=[]

    def load_from_edges(self,n,edges):
        self.g = [[] for _ in range(n)]
        for x, y in edges:
            self.g[x].append(y)
            self.g[y].append(x)  # 建树
        return self
    
    def algo_view(self):
        ret = dict(
            
        )
        def dfs(c,p,v):
            v['title']=f'{self.env.price[c]}'
            v['childs']=[]
            for n in self.g[c]:
                if p==n:continue
                tmp=dict()
                v['childs'].append(tmp)
                dfs(n,c,tmp)
        dfs(0,-1, ret)
        return ret
    
    def hex_str(self):
        return str(self.g)
    
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/difference-between-maximum-and-minimum-price-sum/description/'
    has_view=True
    def get_cases(self):
        return [
            dict(n =4,edges =[[2,0],[0,1],[1,3]],price =[2,3,1,1],result=6),
            dict(n=6, edges=[[0, 1], [1, 2], [1, 3], [3, 4], [
                 3, 5]], price=[9, 8, 7, 6, 10, 5], result=24),
        ]
    
    def main(self):
        return tree(self.g)

    def init(self,n: int, edges: List[List[int]], price: List[int],**kw):
        self.n=n
        self.price = price
        self.g = Graph(self).load_from_edges(n,edges)
        self.ans=0
        self.values=[0]*len(price)


    def execute(self,*args,**kg):
        def dfs(c,p):
            max_c2=0
            for n in self.g.g[c]:
                if n==p:
                    continue
                max_c2=max(dfs(n,c),max_c2)
            return max_c2+self.price[c]
        for i in range(self.n):
            self.ans=max(self.ansd)
        return self.ans
    
    def execute1(self,*args,**kg) -> int:
        self.ans = 0
        def dfs(c,p):
            max_c1=self.price[c]
            max_c2=0
            for n in g[c]:
                if n==p:
                    continue
                max_n1,maxn2=dfs(n,c)
            return max_c1,max_c2            

        return self.ans
 
    def maxOutput(self, *args, **kg):
        self.init(*args,**kg)
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
