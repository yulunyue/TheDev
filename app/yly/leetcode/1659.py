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
            [5,5,6,6,0],
            [2, 3, 1,2,240],
        ]

    def getMaxGridHappiness(self, m: int, n: int, introvertsCount: int, extrovertsCount: int) -> int:
        grid=[[0]*m for _ in range(n)]
        def dfs(ic,ec):
            if ic==0 and ec==0:
                # self.log(grid)
                return 0
            res= 0
            for i in range(n):
                for j in range(m):
                    if grid[i][j]!=0:
                        continue
                    if ic>0:
                        grid[i][j]=1
                        res=max(dfs(ic-1,ec),res)
                    if ec>0:
                        grid[i][j]=2
                        res=max(dfs(ic,ec-1),res)
                    grid[i][j]=0
            return res
        return dfs(introvertsCount,extrovertsCount)
    
    def check(self,*args):
        pass
    
    def test(self,*args):
        return self.xx(*args)

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



