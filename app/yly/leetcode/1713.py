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

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def get_cases(self):
        return [
            [[16,7,20,11,15,13,10,14,6,8],[11,14,15,7,5,5,6,10,11,6],6],
            [[6,4,8,1,3,2],[4,7,6,2,3,8,6,1],3],
            [[5,1,3],[9,4,2,3,4],2],
            
        ]
    
    def minOperations(self, target: List[int], arr: List[int]) -> int:
        a_m=dict()
        for i,a in enumerate(arr):
            if a not in a_m:
                a_m[a]=i
        q=[]
        ret=0
        for w in target:
            if w not in a_m:
                continue
            while q and q[-1]>a_m[w]:
                q.pop()
            q.append(a_m[w])
            ret=max(len(q),ret)
            self.log(w,a_m[w],q)
        return len(target)-ret
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



