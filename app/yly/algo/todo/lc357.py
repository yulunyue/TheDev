from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(n=3,result=739),
            dict(n=4,result=5275)
        ]
    def execute(self, n: int) -> int:
        @functools.lru_cache(None)
        def dfs(i,s,flag):
            if i>=n:
                return 1
            ans=0
            for v in range(10):
                if v==0 and flag:
                    ans+=dfs(i+1,s,flag)
                elif s&(1<<v)==0:
                    ans+=dfs(i+1,s|(1<<v),flag and v==0)
            return ans
        return dfs(0,0,True)
    def countNumbersWithUniqueDigits(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)



if __name__=='__main__':
    Solution().run()