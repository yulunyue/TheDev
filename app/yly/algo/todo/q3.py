from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true
class Solution(SolutionBase):
    uri='https://leetcode.cn/contest/weekly-contest-439/problems/sum-of-k-subarrays-with-length-at-least-m/description/'
    def get_cases(self):
        return [
            dict( nums = [1,2,-1,3,3,4], k = 2, m = 2,result=13)
        ]
    def execute(self, nums: List[int], k: int, m: int) -> int:
        sm=[0]
        for v in nums:
            sm.append(sm[-1]+v)
        n=len(nums)
        @functools.lru_cache(None)
        def dfs(i,k,fill):
            ans=dfs(i+1,k,fill)
            if not fill:
                ans1=sm[i+m+1]-sm[i]+dfs(i+m,k,False)
            else:

            if i+k*m>n+j  or i==n:
                return -inf
            if i+k*m==n+j:
                return sum(nums[i:])        
            ans=dfs(i+1,0,k)
            if j==0:
                tmp=sum(nums[i:i+m])+dfs(i+m,min(i+m,n)-i,k)
            else:
                tmp=nums[i]+max(dfs(i+1,0,k-1),dfs(i+1,j+1,k))
            ans=max(ans,tmp)
            self.log(ans,j,k,nums[i:])
            return ans
            
        return dfs(0,0,False)

    def maxSum(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)



if __name__=='__main__':
    Solution().run()