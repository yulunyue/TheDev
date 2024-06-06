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

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def get_cases(self):
        return [
            [["####F","#C...","M...."], 1, 2,true]
        ]

    def canMouseWin(self, grid: List[str], catJump: int, mouseJump: int) -> bool:
        n = len(grid)
        m = len(grid[0])
        cat=[0,0]
        mouse=[0,0]
        take=[0,0]
        for i in range(n):
            self.log(grid[i])
            for j in range(m):
                if grid[i][j]=='C':
                    cat=[i,j]
                elif grid[i][j]=='M':
                    mouse=[i,j]
                elif grid[i][j]=='F':
                    take=[i,j]
        vt=dict()
        start_state=mouse[0],mouse[1],cat[0],cat[1]
        vt[start_state]=0
        q=[start_state]
        while q:
            p=q
            q=[]
            for my,mx,cy,cx in p:
                pass

        return False
        

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



