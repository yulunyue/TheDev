from common.util.export import MockCf,functools
class Solution(MockCf):
    def totalWaviness(self, num1: int, num2: int) -> int:
        n1=map(str(num1),int)
        n2=map(str(num2),int)
        n=len(n2)
        n1=[0]*(n-len(n1))
        @functools.lrucache(None)
        def dfs(i,lv,ls,lf,rf):
            if i==n: 
                return 0
            ans=0
            la=n1[i] if lf else 0
            ra=n2[i] if rf else 9
            for v in range(la,ra+1):
                llf=rrf=False
                if lf and v==la:
                    llf=True
                if  :wq



        dfs(0,None,None,True,True)
    execute = totalWaviness
