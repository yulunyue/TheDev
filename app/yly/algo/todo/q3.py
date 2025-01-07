from app.yly.algo.manage import SolutionBase,View
from typing import Dict,List
from functools import lru_cache
from collections import defaultdict
from sortedcontainers import SortedList,SortedDict
import bisect
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(coins = [[1,10,3]], k = 2,result=6),
            dict( coins = [[8,10,1],[1,3,2],[5,6,4]], k = 4,result=10.1),
        ]


    def maximumCoins(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute()
    def init(self, coins: List[List[int]], k: int) -> int:
        self.coins=sorted(coins)
        self.k=k

    def execute(self):
        ret=tmp_sum=0
        li=0
        n=len(self.coins)
        for i in range(n):
            l,r,c=self.coins[i]
            ln=r-l+1
            if r<=self.k:
                tmp_sum+=ln*c
                ret=tmp_sum
            else:
                while li<=i:
                    l1,r1,c1=self.coins[li]
                    if r-l1<=self.k:
                        break
                    v1=(self.k-l+l1)*c
                    ret=max(ret,tmp_sum+v1)
                    v2=ln*c-min(r-l1-self.k+1,r1-l1+1)*c1
                    ret=max(ret,tmp_sum+v2)
                    li+=1
                    tmp_sum+=v2
                    self.log(ret,l1,r1,l,r,v1,v2)
                    
  
        return ret





if __name__=='__main__':
    Solution().run()