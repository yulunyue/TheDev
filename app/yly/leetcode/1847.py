from typing import List,Dict,Optional
from collections import defaultdict, deque,Counter
from itertools import accumulate,product
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf=float("inf")
null=None
true=True
false=False
M=10**9 + 7


class Solution:
    def get_cases(self):
        return [
            [[[1,4],[2,3],[3,5],[4,1],[5,2]],  [[2,3],[2,4],[2,5]],[2,1,3]],
        ]

    def closestRoom(self, rooms: List[List[int]], queries: List[List[int]]) -> List[int]:
        rooms=sorted([[v[1],v[0]] for i,v in enumerate(rooms)])
        ret=[-1]*len(queries)
        queries=sorted([[v[1],v[0],i] for i,v in enumerate(queries)])
        l=0
        sort_id=sorted([v[1] for v in rooms])
        self.log(rooms)
        self.log(queries)
        self.log(sort_id)
        for min_size,index,idx in queries:
            l1=bisect.bisect_left(rooms,[min_size,0],lo=l)
            if l>=len(rooms):
                break
            for i in range(l,l1):
                remove_id=bisect.bisect_left(sort_id,rooms[i][0])
                sort_id.pop(remove_id)
            self.log(sort_id,min_size,l1,index)
            li=bisect.bisect_left(sort_id,index)
            ri=bisect.bisect_right(sort_id,index)
            if ri>=len(sort_id) or index-sort_id[li]<=sort_id[ri]-index:
                ret[idx]=sort_id[li]
            else:
                ret[idx]=sort_id[ri]
            l=l1
        return ret
    def check(self,*args):
        pass
    
    def test(self,*args):
        return self.closestRoom(*args)

    def init(self,*args):
        pass

    def __init__(self,*args) -> None:
        self.local_debug=getattr(self,sys.argv[-1],None)
        self.init(*args)
        if self.local_debug is None:
            print(sys.argv[-1],"not find")
    logs = ""
    def log(self, *s):
        if not self.local_debug or len(self.logs)>=2048:
            return
        self.logs += " ".join([str(v) for v in s])+"\n"
    
    def run(self):
        if not self.local_debug:
            return
        for case in self.get_cases():
            self.logs=""
            try:
                r=self.local_debug(*case[:-1])
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r=None
            if not self.diff(r,case[-1]):
                self.check(*case,r)
                print(case,r)
                print(self.logs)
                break
            
    def diff(self,a,b):
        if isinstance(a,float) and isinstance(b,float):
            return "%.2f"%(a)=="%.2f"%(b)
        return a==b

    



      

if __name__ == '__main__':
    Solution().run()



