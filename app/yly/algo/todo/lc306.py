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
            c=0
            k=i2-i1
            i0=i1-k
            
            for m in range(k):
                a2,a3=num[i2-m],num[i1-m]-c
                if a3>a2:
                    a1=a3-a2
                    c=0
                else:
                    a1=a3+10-a2
                    c=1
           
                return False
            
                
        @functools.lru_cache(None)
        def dfs0(j):
            for i in range(j+1):
                if dfs1(i,j):
                    return True
            return False
        return dfs0(n-1)

    def isAdditiveNumber(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
  



if __name__=='__main__':
    Solution().run()