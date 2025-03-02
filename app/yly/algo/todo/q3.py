from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true
class Solution(SolutionBase):
    uri='https://leetcode.cn/contest/weekly-contest-439/problems/sum-of-k-subarrays-with-length-at-least-m/description/'
    def get_cases(self):
        return [
            dict( nums = [1,2,-1,3,3,4], k = 2, m = 2,result=13)
        ]
    def execute(self, nums: List[int], k: int, m: int) -> int:
        pass

    def maxSum(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)



if __name__=='__main__':
    Solution().run()