
from app.yly.algo.manage import SolutionBase
from typing import Dict,List
from functools import lru_cache
from common.algo.unifind import UniFind
MOD=(10**9)+7
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/count-connected-components-in-lcm-graph/description/'
    def get_cases(self):
        return [
            dict(nums = [2,4,8,3,9,12], threshold = 10,result=2),
            dict(nums =[4,31,35],threshold =129,result=2),
        ]
    

    def init(self, nums: List[int], threshold: int,**kw) -> int:
        self.idx = {}
        self.uf=UniFind()
        self.threshold = threshold
        self.ans=len(nums)
        for i,v in enumerate(nums):
            if v<=threshold:
                self.idx[v]=i


    def execute(self):
        for g in range(1,self.threshold+1):
            fi=-1
            x=g
            while x<=self.threshold:
                if x in self.idx:
                    fi=self.uf.find(self.idx[x])
                    break
                x+=g
            if fi==-1:
                continue
            max_v=g*self.threshold//x+1
            for y in range(x+g,max_v,g):
                if y in self.idx:
                    _,f=self.uf.merge(fi,self.idx[y])
                    self.ans-=f
        return self.ans
    
    def countComponents(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute()

if __name__=='__main__':
    Solution().run()