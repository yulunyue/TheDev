from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/separate-squares-ii/description/'
    def get_cases(self):
        return [
            dict(squares = [[0,0,1],[2,2,1]],result=1.00000),
            dict(squares = [[0,0,2],[1,1,1]],result=1.00000)
        ]
    
    def separateSquares(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
    def execute(self,squares):
        n=len(squares)
        sc=10000
        mx,mn=-inf,inf
        for i in range(n):
            squares[i][1]*=sc
            mx=max(squares[i][1]+squares[i][2]*sc,mx)
            mn=min(squares[i][1],mn)
        def check(h):
            up,low=0,0
            for _,y,c in squares:
                up+=max(y-h+sc*c,0)*c
                low+=max(h-y,0)*c
            # self.log(h,low,up)
            return low>=up-1
        return (bisect.bisect_left(range(mn,mx),True,key=check)+mn)/sc



if __name__=='__main__':
    Solution().run()