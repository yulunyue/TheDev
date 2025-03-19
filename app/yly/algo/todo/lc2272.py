from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(s = "aababbb",result=3),
        ]
    def execute(self, s: str) -> int:
        n=len(s)
        g=[[0]*26 for _ in range(n+1)]
        for i,v in enumerate(s):
            o=ord(v)-ord('a')
            for j in range(26):
                g[i+1][j]=g[i][j]+(j==o)
        a=0
        for i in range(26):
            for j in range(26):
                b=g[1][i]-g[1][j]
                for k in range(2,n+1):
                    c=g[k][j]-g[k][i]
                    a=max(a,c-b)
                    b=min(b,-c)
        return a
    def largestVariance(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)



if __name__=='__main__':
    Solution().run()