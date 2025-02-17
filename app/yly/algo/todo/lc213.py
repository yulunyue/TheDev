from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(nums = [2,3,2],result=3),
        ]
    
    def rob(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
    def execute(self, nums: List[int]) -> int:   
        pass



if __name__=='__main__':
    Solution().run()