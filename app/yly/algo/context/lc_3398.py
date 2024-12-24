from app.yly.algo.manage import SolutionBase,View
from typing import Dict,List
from functools import lru_cache
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(s = "000001", numOps = 1,result=2),
        ]
    def init(self, s: str, numOps: int,**kw) -> int:
        self.s,self.num_ops=s+'#',numOps
        self.n=len(self.s)

    def minLength(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute()
        
    def execute(self):
        a=[0]
        for i,v in enumerate(self.s):
            if i and v!=self.s[i-1]:
                a.append(i)
        self.log(a)


if __name__=='__main__':
    Solution().run()