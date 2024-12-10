from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from sortedcontainers import SortedList
from functools import lru_cache
import bisect
import sys
import math
import heapq
from app.yly.algo.manage import SolutionBase,View
from common.algo.graph import Graph

class G(Graph):
    def init(self):
        self.sum_v1=defaultdict(int)
        self.sum_v2=defaultdict(int)
    
    def get_title_key(self):
        return ['sum_v1','sum_v2','value']
    
    def __str__(self):
        return f'{self.value}{self.g}{self.sum_v1}{self.sum_v2}'

class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/difference-between-maximum-and-minimum-price-sum/description/'
    _has_view=True
    def get_cases(self):
        return [
            dict(n=6, edges=[[0, 1], [1, 2], [1, 3], [3, 4], [
                 3, 5]], price=[9, 8, 7, 6, 10, 5], result=24),
            dict(n =4,edges =[[2,0],[0,1],[1,3]],price =[2,3,1,1],result=6),
  
        ]
    
    def get_watch(self):
        return [
            View().add_node(
                View("ans"),
                View("result"),
            ),
            View('root',size=32).graph()
        ]


    def init(self,n: int, edges: List[List[int]], price: List[int],result=0,**kw):
        self.result=0
        self.root = G().set_values(
            price
        ).load_from_edges(
            edges
        )
        self.ans=result

    def execute(self):
        def dfs(c,p=None):
            self.root.sum_v1[c]=self.root.value[c]
            self.root.sum_v2[c]=0
            for n,*args in self.root.g[c]:
                if n==p:
                    continue
                c1,c2=dfs(n,c)
                self.result = max(
                    self.result,
                    self.root.sum_v1[c]+c2,
                    self.root.sum_v2[c]+c1
                )
                self.root.sum_v1[c]=max(self.root.sum_v1[c],c1+self.root.value[c])
                self.root.sum_v2[c]=max(self.root.sum_v2[c],c2+self.root.value[c])

            return self.root.sum_v1[c],self.root.sum_v2[c]

        dfs(0)
        return self.result

 
    def maxOutput(self, *args, **kg):
        self.init(*args,**kg)
        return self.execute()


if __name__ == '__main__':
    Solution().run()
