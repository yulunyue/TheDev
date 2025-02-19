from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(ax1 = -3, ay1 = 0, ax2 = 3, ay2 = 4, bx1 = 0, by1 = -1, bx2 = 9, by2 = 2,result=45),
        ]
    
    def computeArea(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
    def execute(self, ax1: int, ay1: int, ax2: int, ay2: int, bx1: int, by1: int, bx2: int, by2: int) -> int:
        ans=(ay2-ay1)*(ax2-ax1)+(by2-by1)*(bx2-bx1)
        if ax2<=bx1 or bx2<=ax1:
            return ans
        if ay2<=by1 or by2<=ay1:
            return ans
        y=min(ay2,by2)-max(ay1,by1)
        x=min(ax2,bx2)-max(ax1,bx1)
        return ans-y*x



if __name__=='__main__':
    Solution().run()