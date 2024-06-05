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
            [["acca","bbbb","caca"], "aba",6],
        ]
    def numWays(self, words: List[str], target: str) -> int:
        m=len(words[0])
        k=len(target)
        wc=[defaultdict(int) for _ in range(m)]
        for word in words:
            for i in range(m):
                wc[i][word[i]]+=1

        @lru_cache(None)
        def dfs(i,j):
            if j>=k:
                return 1
            if i>=m:
                return 0
            res=dfs(i+1,j)
            if wc[i][target[j]]:
                res+=wc[i][target[j]]*dfs(i+1,j+1)
            return res%M
            
        return dfs(0,0)


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



