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
            [3, [1,2,3,4,5],[5,2,3,3,3] ,[1]]
        ]
    def busiestServers(self, k: int, arrival: List[int], load: List[int]) -> List[int]:
        avaliable=list(range(k))
        busy=[]
        id_count=[0]*k
        for i,v in enumerate(arrival):
            while busy and busy[0][0]<=v:
                _,n_id=heapq.heappop(busy)
                avaliable.insert(bisect.bisect_left(avaliable,n_id),n_id)
                self.log(avaliable)
            if not avaliable:
                continue
            j=bisect.bisect_left(avaliable,i%k)
            if j==len(avaliable):
                j=0
            idx=avaliable[j]
            heapq.heappush(busy,(v+load[i],idx))
            id_count[idx]+=1
            avaliable.pop(j)
        max_id=max(id_count)
        return [i for i in range(k) if id_count[i]==max_id]

    def test(self,*args):
        return self.busiestServers(*args)
            

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



