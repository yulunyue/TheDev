from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(num="112358",result=True),
            dict(num="199100199",result=True)
        ]
    def execute(self, num: str) -> bool:
        num=[int(v) for v in num]
        dt=dict()
        n=len(num)
        for i in range(n):
            a=0
            for j in range(i,n):
                a=a*10+num[j]
                dt[i,j]=a
        

        @functools.lru_cache(None)
        def dfs2(i,v):
            self.log(f'sum0 {num[:i+1]},{v}')
            b,c=0,1
            while i>=0:
                b+=num[i]*c
                c*=10
                if b==v:
                    return i-1
                if b>v:
                    return -2 
                i-=1
            
            return -2
        @functools.lru_cache(None)
        def dfs1(i,v):
            self.log(f'sum1 {num[:i+1]},{v}')
            b,c=0,1
            while i>=0:
                b+=num[i]*c
                c*=10
                if b>v:
                    return False
                j=dfs2(i-1,v-b)
                if j==-1:
                    return True
                if j>=0 and dfs0(j):
                    return True
                i-=1
        @functools.lru_cache(None)
        def dfs0(i):
            self.log(f'sum2 {num[:i+1]}')
            b,c=0,1
            while i>=0:
                b+=num[i]*c
                c*=10
                if dfs1(i-1,b):
                    return True
                i-=1
            return False
        return dfs0(n-1)

    def isAdditiveNumber(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
  



if __name__=='__main__':
    Solution().run()