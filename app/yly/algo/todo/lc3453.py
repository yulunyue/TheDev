from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(sequares=[[0,0,2],[1,1,1]],result=1.16667)
        ]
    
    def seprateSequares(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
    def execute(self,sequares):
        n=len(sequares)
        sc=10000
        mx,mn=-inf,inf
        for i in range(n):
            sequares[i][1]*=sc
            mx=max(sequares[i][1]+sequares[i][2]*sc,mx)
            mn=min(sequares[i][1],mn)
        def check(h):
            up,low=0,0
            for _,y,c in sequares:
                up+=max(y-h+sc*c,0)*c
                low+=max(h-y,0)*c
            # self.log(h,low,up)
            return low>=up-1
        return (bisect.bisect_left(range(mn,mx),True,key=check)+mn)/sc



if __name__=='__main__':
    Solution().run()