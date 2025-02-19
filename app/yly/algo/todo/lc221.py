from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/maximal-square/'
    def get_cases(self):
        return [
             dict(matrix = [["1"]],result=1),
            dict(matrix = [["0"]],result=0),
            dict(matrix =[["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]],result=4),
        ]
    
    def maximalSquare(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
    def execute(self, matrix: List[List[str]]) -> int:
        n,m=len(matrix),len(matrix[0])
        g=[[0]*(m+1) for _ in range(n+1)]
        for i in range(n):
            for j in range(m):
                g[i+1][j+1]=g[i][j+1]+g[i+1][j]-g[i][j]+(matrix[i][j]=='1')
        def check(v):
            # b=-inf
            for i in range(v,n+1):
                for j in range(v,m+1):
                    top,left=i-v,j-v
                    a=g[i][j]+g[top][left]-g[i][left]-g[top][j]
                    if a==v*v:
                        return False
            # self.log(v,b)
            return True
        a=bisect.bisect_left(range(0,min(n,m)+1),True,key=check)-1
        return a*a
        



if __name__=='__main__':
    Solution().run()