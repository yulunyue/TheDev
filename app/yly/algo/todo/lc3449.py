from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,math
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(points = [5,3], m = 8,result=12),
            dict(points = [1,8],m=10,result=5),
            dict(points = [2,4], m = 3,result=4),
            
            
        ]
    
    def execute(self, points: List[int], m: int) -> int:
        if m<len(points):
            return 0
        n=len(points)
        mn=(m+1)//2*min(points)
        def check(v):
            m1=m
            pre=0
            for i,u in enumerate(points):
                k = v//u+1-pre
                if i==n-1 and k<=0:
                    return False
                
            return False
        return bisect.bisect_left(range(mn),True,key=check)


    def maxScore(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        


if __name__=='__main__':
    Solution().run()