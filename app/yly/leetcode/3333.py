

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")
MOD=(10**9)+7
try:
    from app.yly.manage import SolutionBase

except:
    class SolutionBase:
        def input(self):
            return input()

        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass

        def run(self):
            pass



class Solution(SolutionBase):
    uri = "hhttps://leetcode.cn/problems/find-the-original-typed-string-ii/description/"
    gameid = ''

    def get_cases(self):
        return [
            dict(word = "aabbccdd", k = 7,result=5),
        ]
    def execute(self, word: str, k: int) -> int:
        n=len(word)
        s=[]
        ct=1
        last_ct=1
        for i in range(1,n):
            if word[i]==word[i-1]:
                ct+=1
            else:
                s.append([last_ct,ct,i])
                last_ct=(last_ct*ct)%MOD
                ct=1
        s.append([last_ct,ct,n])
        # self.log(s)
        @lru_cache(None)
        def dfs(i,k):
            if i==-1:
                return k==0
            ct,ci,cn=s[i]
            if cn<=k:
                return 1 if cn==k else 0
            ans=0
            if ci>=k:
                ans=(ans+(ci-k+1)*ct)%MOD
            for j in range(1,min(ci+1,k)):
                ans+=dfs(i-1,k-j)
            # self.log(i,k,ans)
            return ans%MOD
        return dfs(len(s)-1,k)
    def possibleStringCount(self,*args,**kg):
        return self.execute(*args,**kg)


if __name__ == '__main__':
    Solution().run()
