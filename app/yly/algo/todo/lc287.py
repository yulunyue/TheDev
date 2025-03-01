from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/find-the-duplicate-number/'
    def get_cases(self):
        return [
            dict(nums =[2,5,9,6,9,3,8,9,7,1],result=9),
             dict(nums = [3,1,3,4,2],result=3),
            dict(nums = [1,3,4,2,2],result=2),
            dict(nums = [3,3,3,3,3],result=3),
           
        ]
    def execute(self, nums: List[int]) -> int:
        # self.log(nums)
        # self.log(list(range(len(nums))))
        p1,p2=nums[0],nums[nums[0]]
        while p1!=p2:
            p1,p2=nums[p1],nums[nums[p2]]
        p1=nums[p1]
        p2=nums[0]
        self.log(p1,p2)
        while p1!=p2:
            p1,p2=nums[p1],nums[p2]
        # for _ in range(n):
        #     a=nums[a]
        return p1
    def findDuplicate(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        




if __name__=='__main__':
    Solution().run()