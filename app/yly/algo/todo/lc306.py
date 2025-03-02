from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(num="112358",result=True),
            dict(num="199100199",result=True)
        ]
    def execute(self, num: str) -> bool:
        num=[int(v) for v in num]
        n=len(num)
        @functools.lru_cache(None)
        def dfs1(i1,i2):
            i0=2*i1-i2
            last_c=0
            for i in range(i2-i1):
                a,b,c=num[i0-i],num[i1-i],num[i2-i]
                if (a+b)%10==last_c+c:
                    pass 
        
            
                
        @functools.lru_cache(None)
        def dfs0(j):
            for i in range(j):
                if dfs1(i,j):
                    return True
            return False
        return dfs0(n-1)

    def isAdditiveNumber(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
  



if __name__=='__main__':
    Solution().run()