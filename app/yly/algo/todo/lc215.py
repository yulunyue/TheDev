from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/kth-largest-element-in-an-array/'
    def get_cases(self):
        return [
            dict(nums=[3,2,1,5,6,4], k = 2,result=5),
            dict(nums=[3,2,3,1,2,4,5,5,6], k = 4,result=4)
        ]
    
    def findKthLargest(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
    def execute(self, nums: List[int], k: int) -> int:
        max_num=max(nums)
        ct=[0]*(max_num+1)
        for v in nums:
            ct[v]+=1
        n=len(ct)-1
        while n>=0 and k:
            k-=ct[n]
            if k<=0:
                break
            n-=1
        return n



if __name__=='__main__':
    Solution().run()