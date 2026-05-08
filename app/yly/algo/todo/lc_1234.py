from common.util.export import List, Dict, functools, CT


class Solution:
    def balancedString(self, s: str) -> int:
        c = dict(Q=0, W=0, E=0, R=0)
        ci,cj=c.copy(),c.copy()
        for v in s:
            c[v]+=1
        n = len(s)
        m=n//4
        
        j=0
        ans=n
        for i,v in enumerate(s):
            while j<n and not check():
                cj[j]+=1
            ans=min(ans,j-i)
            ci[v]+=1        
        return ans
