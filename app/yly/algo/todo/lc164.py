from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,math
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(nums=[3,6,9,1],result=3)
        ]
    
    def findPeekElement(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
    def execute(self,nums:List[int],**kw):
        n=len(nums)
        mn,mx=min(nums),max(nums)
        if n==1:
            return 0
        size=ans=(mx-mn)/(n-1)
        bucket=[[inf,-inf] for _ in range(n)]
        for v in nums:
            idx=int((v-mn)/size)
            bucket[idx][0]=min(bucket[idx][0],v)
            bucket[idx][1]=max(bucket[idx][1],v)
        last_max=None
        for i in range(n):
            if bucket[i]==[inf,-inf]:
                continue
            if last_max:
                ans=max(ans,bucket[i][0]-last_max)
            last_max=bucket[i][1]
        return ans
            



if __name__=='__main__':
    Solution().run()