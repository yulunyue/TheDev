from sortedcontainers import SortedList
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
            [[[1,2],[2,1],[4,3],[7,2]],[1,-1,3,-1]]
        ]

    def test(self, cars_pos:List[List[int]]):
        n=len(cars_pos)
        cars_pos = sorted([[cars_pos[i][0],cars_pos[i][1],i] for i in range(n)])
        ret = [-1]*n
        while len(cars_pos):
            min_time,min_idx=inf,None
            for i in range(1,len(cars_pos)):
                speed_c=cars_pos[i-1][1]-cars_pos[i][1]
                if speed_c<=0:
                    continue
                user_time=(cars_pos[i][0]-cars_pos[i-1][1])/speed_c
                if user_time<min_time:
                    min_time=user_time
                    min_idx=i
            if min_idx is None:
                break
            ret[cars_pos[i][2]]=min_time
            cars_pos.pop(min_idx)
            break
        return ret

    def check(self,*args):
        pass

    def __init__(self) -> None:
        self.local_debug=getattr(self,sys.argv[-1],None)
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



