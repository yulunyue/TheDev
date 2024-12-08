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
    from app.yly.algo.manage import SolutionBase,View,UniFind,Graph
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


class Solution(SolutionBase):
    _has_view=True
    def get_cases(self):
        return [
            dict(vals=[1, 3, 2, 1, 3], edges=[
                 [0, 1], [0, 2], [2, 3], [2, 4]], result=6)
        ]
    
 

    def init(self, vals: List[int], edges: List[List[int]],result=0):
        self.ans=result
        self.graph=Graph().load_from_edges(edges)
        self.uf=UniFind(len(vals))
        self.result=0
        self.vals = vals
        self.nums=sorted([[v, i] for i, v in enumerate(vals)])
    
    def get_watch(self):
        return [
            View().add_node(
                View("ans"),
                View("vals"),
                View("nums"),
                View("result")
            ),
            View().add_node(
                View("uf",size=10).tree(),
                View("graph",size=10).graph()
            )
        ]
    
    def execute(self,**kw):
        for v, pid in self.nums:
            ppid = self.uf.find(pid)
            for pnid,*args in self.graph.g[pid]:
                pnid = self.uf.find(pnid)
                if self.vals[pnid] > v or pnid == ppid:
                    continue
                if self.vals[pnid] == v:
                    self.result += self.uf.size[ppid]*self.uf.size[pnid]
                self.uf.merge(ppid,pnid)
        return self.result

    def numberOfGoodPaths(self, *args, **kg) -> int:
        self.init(*args,**kg)
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
