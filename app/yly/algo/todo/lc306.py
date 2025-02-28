from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(num="112358",result=True)
        ]
    def execute(self, num: str) -> bool:
        num=[int(v) for v in num]
        n=len(num)

        @functools.lru_cache(None)
        def dfs2(i,v):
            b=0
            while i>=0:
                b=b*10+num[i]
                if b==v:
                    return i-1
                if b>v:
                    return -2 
                i-=1
            return -2
        @functools.lru_cache(None)
        def dfs1(i,v):
            b=0
            while i>=0:
                b=b*10+num[i]
                if b>v:
                    return False
                j=dfs2(i-1,v-b)
                if j==-1:
                    return True
                if j>=0 and dfs1(j,num[j]):
                    return True
                i-=1
        a=0
        for i in range(n-1,-1,-1):
            a=a*10+num[i]
            if dfs1(i-1,a):
                return True
        return False

    def isAdditiveNumber(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
  



if __name__=='__main__':
    Solution().run()