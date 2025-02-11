from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(nums=[3,6,9,1],result=3)
        ]
    
    def findPeekElement(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
    def execute(self,nums,**kw):
        l,r=0,len(nums)-1
        while l<r:
            m=(l+r)//2
            if m+1<len(nums) and nums[m]<nums[m+1]:
                l=m+1
            elif m>=1 and nums[m]<nums[m-1]:
                r=m-1
            else:
                return m
        
            



if __name__=='__main__':
    Solution().run()