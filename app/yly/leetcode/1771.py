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
            ["cfe","ef",4],
            ["cacb","cbba",5],
            ["aa","bb",0],
        ]
    def longestPalindrome(self, word1: str, word2: str) -> int:
        s1=defaultdict(list)
        s=word1+word2
        for i,v in enumerate(s):
            s1[v].append(i)
        @lru_cache(None)
        def dfs(i,j):
            if i==j:
                return 1
            if i>j:
                return 0
            self.log(s[i:j+1])
            if s[i]==s[j]:
                return 2+dfs(i+1,j-1)
            return max(dfs(i+1,j),dfs(i,j-1))
    
        res=-inf
        for i,v in enumerate(word1):
            if s1[v] and s1[v][-1]>=len(word1):
                res=max(2+dfs(i+1,s1[v][-1]-1),res)
                s1[v]=[]
        return 0 if res==-inf else res

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



