from app.yly.algo.manage import SolutionBase,View
from typing import Dict,List
from functools import lru_cache
from collections import defaultdict
import bisect
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(s = "110", k = 3,result=-1),
            dict(s = "12233", k = 4,result=-1),
        ]
    
    def maxDifference(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
    
    def execute(self, s: str, k: int) -> int:
        '''
        max(a[i]-a[j]-(b[i]-b[j]))
        max(c[i]-min(-c[:i-k]))
        '''
        ans=-inf
        s=[int(v) for v in s]
        for i in range(5):
            for j in range(5):
                if i==j:
                    continue
                pres=[0]*5
                curs=[0]*5
                mins=[[inf,inf],[inf,inf]]
                l=0
                for r,v in enumerate(s):
                    curs[v]+=1
                    while l+k<r:
                        p,q=pres[i]&1,pres[j]&1
                        mins[p][q]=min(mins[p][q],pres[j]-pres[i])
                        pres[s[l]]+=1
                        l+=1
                    if r>=k:
                        minqp=minqp
                        ans=max(ans,curs[i]-curs[j])
        return ans




if __name__=='__main__':
    Solution().run()