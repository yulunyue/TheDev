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
    
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/difference-between-maximum-and-minimum-price-sum/description/'
    has_view=True
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
            ),
            View('root').graph()
        ]


    def init(self,n: int, edges: List[List[int]], price: List[int],result=0,**kw):
        self.root = Graph(
            self
        ).set_values(
            price
        ).load_from_edges(
            edges
        )
        self.ans=result

    def execute(self):
        def dfs(c,p=None):
            sum_c1=self.root.value[c]
            sum_c2=0
            for n,*args in self.root.g[c]:
                if n==p:
                    continue
                c1,c2=dfs(n,c)
      
            return sum_c1,sum_c2

        return dfs(0)

 
    def maxOutput(self, *args, **kg):
        self.init(*args,**kg)
        return self.execute()


if __name__ == '__main__':
    Solution().run()
