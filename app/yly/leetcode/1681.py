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
            [[6,3,8,1,3,1,2,2],4,6],
            [[5,3,3,6,3,3], 3,-1]
        ]
    
    def minimumIncompatibility(self, nums: List[int], k: int) -> int:
        k = len(nums)//k
        if k==1:
            return 0
        nums.sort()
        rp=defaultdict(int)
        n=len(nums)
        ret=0
        tmp=[]
        def add(array:List,v):
            array.append(v)
            ret=0
            if len(array)==k:
                ret=array[-1]-array[0]
                array.clear()
            return ret
        def clear(tmp):
            ret=0
            for k1 in list(rp.keys()):
                rp[k1]-=1
                ret+=add(tmp,k1)
                if rp[k1]==0:
                    rp.pop(k1)
            return ret
        for i in range(n):
            if tmp and nums[i]==tmp[-1]:
                rp[nums[i]]+=1
            else:
                add_v=add(tmp,nums[i])
                ret+=add_v
                if add_v>0:
                    ret+=clear(tmp)
            self.log(i,nums[i],tmp,ret,rp)
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



