# from sortedcontainers import SortedList
from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7




class Solution:
    def get_cases(self):
        return [
            [[[1,13],[1,1],[2,10,5],[1,9],[2,15,6]],[true,true]],
            [[[1, 6], [1, 1], [2, 7, 5]], [true]],
            [[[1, 7], [1, 6], [2, 4, 9], [1, 11], [2, 11, 5]], [false, true]],
            [[[1, 1], [1, 11], [1, 4], [1, 8], [2, 13, 7]], [False]],
            [[[1, 3], [2, 4, 2]], [true]],
            [[[1, 2], [2, 3, 3], [2, 3, 1], [2, 2, 2]], [false, true, true]],
            [[[1, 7], [2, 7, 6], [1, 2], [2, 7, 5], [2, 7, 6]], [true, true, false]]
        ]

    def getResults(self, queries: List[List[int]]) -> List[bool]:
        max_id = max(v[1] for v in queries)+1
        ol=[0]*(max_id*4)
        wall_ids = [0, max_id]
        
        def update(o,l,r,i,v):
            if l==r:
                ol[o]=v
                return
            m=(l+r)//2
            if i<=m:
                update(o*2,l,m,i,v)
            else:
                update(o*2+1,m+1,r,i,v)
            ol[o]=max(ol[o*2],ol[o*2+1])
        def query(o,l,r,i):
            if r<=i:
                return ol[o]
            m=(l+r)//2
            if i<=m:
                return query(o*2,l,m,i)
            return max(ol[o*2],query(o*2+1,m+1,r,i))
        def set_wall(x):
            l = bisect.bisect_left(wall_ids, x)
            self.log("update",wall_ids[l],wall_ids[l]-x)
            self.log("update",x, x-wall_ids[l-1])
            update(1,1, max_id, wall_ids[l],wall_ids[l]-x)
            update(1,1, max_id, x, x-wall_ids[l-1])
            wall_ids.insert(l, x)

        def query2(x, w):
            if x < w:
                return False
            
            l = bisect.bisect_left(wall_ids, x)
            # self.log(wall_ids[l-1],ol,query(1, 1,max_id,wall_ids[l-1]))
            return x-wall_ids[l-1] >= w or query(1, 1,max_id,wall_ids[l-1]) >= w

        ret = []
        for tp, *args in queries:
            if tp == 1:
                set_wall(*args)
            else:
                ret.append(query2(*args))
        return ret
    def test(self,*args,**kwargs):
        return self.getResults(*args,**kwargs)
    def check(self, *args):
        pass

    def __init__(self) -> None:
        self.local_debug = getattr(self, sys.argv[-1], None)
        if self.local_debug is None:
            print(sys.argv[-1], "not find")
    logs = ""

    def log(self, *s):
        if not self.local_debug or len(self.logs) >= 2048:
            return
        self.logs += " ".join([str(v) for v in s])+"\n"

    def run(self):
        if not self.local_debug:
            return
        for case in self.get_cases():
            self.logs = ""
            try:
                r = self.local_debug(*case[:-1])
            except Exception as e:
                import traceback
                traceback.print_exc()
                r = None
            if not self.diff(r, case[-1]):
                self.check(*case, r)
                print(case, r)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution().run()
