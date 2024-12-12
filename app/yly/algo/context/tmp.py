from app.yly.algo.manage import SolutionBase
from typing import Dict,List
import heapq
from functools import lru_cache
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(values = [[8,5,2],[6,4,1],[9,7,3]],result=285)
        ]
    

    def init(self, values: List[List[int]],**kw) -> int:
        self.values = values
    
    def execute(self):
        self.ans=0
        h=[]
        for values in self.values:
            heapq.heappush(values.pop())
        

    def maxSpending(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute()

if __name__=='__main__':
    Solution().run()