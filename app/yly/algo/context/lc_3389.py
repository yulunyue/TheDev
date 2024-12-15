from app.yly.algo.manage import SolutionBase
from collections import defaultdict
from common.algo.str_util import z_kmp
from typing import Dict,List
import heapq
from functools import lru_cache
import math
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(s='acab',result=1)
        ]

    def init(self, s:str):
        self.ct=[0]*26
        ord_a=ord('a')
        for v in s:
            self.ct[ord(v)-ord_a]+=1
        self.max_ct=max(self.ct)
        self.min_ct=min(self.ct)

    def execute(self):
        def get(p):
            @lru_cache(None)
            def dfs(i):
                if i>=26:
                    return 0
                t1 = min(
                    self.ct[i],
                    abs(self.ct[i]-p)
                )+dfs(i+1)
                t2=inf
                if i+1<26:
                    for g1 in [self.ct[i],self.ct[i]-p]:
                        for g2 in [self.ct[i+1],self.ct[i+1]-p]:
                            t3=abs(g1)+abs(g2)
                            if g1>0 and g2<0:
                                t3-=min(g1,-g2)
                            t2=min(t2,t3)
                return min(t1,t2+dfs(i+2))
            return dfs(0)
        res=inf
        for i in range(self.min_ct,self.max_ct+1):
            res=min(res,get(i))
        return res
    def makeStringGood(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute()

if __name__=='__main__':
    Solution().run()