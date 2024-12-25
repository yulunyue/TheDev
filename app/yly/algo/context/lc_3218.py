from app.yly.algo.manage import SolutionBase,View
from typing import Dict,List
from functools import lru_cache
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(m =7,n =4,horizontalCut =[13,6,12,14,4,7],verticalCut =[14,15,11],result=258),
            dict(m =6,n =3,horizontalCut =[2,3,2,3,1],
verticalCut =[1,2],
result=28),
            dict(m =1,n =7,horizontalCut =[],verticalCut =[2,1,2,1,2,1],result=9),
            dict(m = 3, n = 2, horizontalCut = [1,3], verticalCut = [5],result=13),
        ]
    
    def init(self, m: int, n: int, horizontalCut: List[int], verticalCut: List[int],**kw) -> int:
        self.m = m
        self.n = n
        self.horizontalCut = sorted(horizontalCut)
        self.verticalCut = sorted(verticalCut)
    
        
    def minimumCost(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute()
    
    def execute(self):
        ans = i = j = 0
        for _ in range(self.m+self.n-2):
            if j == self.n-1 or i<self.m-1 and self.horizontalCut[i]<self.verticalCut[j]:
                ans+=self.horizontalCut[i]*(self.n-j)
                i+=1
            else:
                ans+=self.verticalCut[j]*(self.m-i)
                j+=1
            # self.log(i,j)
        return ans


if __name__=='__main__':
    Solution().run()