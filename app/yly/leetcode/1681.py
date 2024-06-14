from sortedcontainers import SortedList
from typing import List,Dict,Optional
from collections import defaultdict, deque,Counter
from itertools import accumulate,product
from functools import lru_cache
import itertools
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
            [[1,2,1,4],2,4],
             [[6,3,8,1,3,1,2,2], 4,6],
            [[12,5,16,7,13,4,3,14,4,11,8,6,6,1,15,12],4,0],
            [[5,3,3,6,3,3], 3,-1]
        ]

    def minimumIncompatibility(self, nums: List[int], k: int) -> int:
        n = len(nums)
        m = n // k
        if m==1:
            return 0
        nm=defaultdict(int)
        for n in nums:
            nm[n]+=1
        keys=sorted(nm.keys())
        ret=0
        for _ in range(k):
            j=0
            s=[]
            while j<m:
                if nm[keys[j]]==0:
                    keys.pop(j)
                else:
                    s.append(keys[j])
                    nm[keys[j]]-=1
                    j+=1
            self.log(s)
            ret+=s[-1]-s[0]
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



