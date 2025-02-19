from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/length-of-longest-v-shaped-diagonal-segment/description/'
    def get_cases(self):
        return [
            dict(grid=[[2,2,1,2,2],[2,0,2,2,0],[2,0,1,1,0],[1,0,2,2,2],[2,0,0,2,2]],result=5),
            dict(grid = [[2,2,2,2,2],[2,0,2,2,0],[2,0,1,1,0],[1,0,2,2,2],[2,0,0,2,2]],result=4),
        ]
    
    def lenOfVDiagonal(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
    def execute(self, grid,**kw):
        n,m=len(grid),len(grid[0])
        dr=[[1,1],[-1,1],[-1,-1],[1,-1]]

        @functools.lru_cache(None)
        def dfs(i,j,y,x,not_use):       
            d=[[y,x]]
            if not_use:
                d.extend([[1,-1],[-1,1]] if y==x else [[1,1],[-1,-1]])
            ans=0
            for dy,dx in d:
                ny,nx=i+dy,j+dx
                if ny<0 or nx<0 or ny==n or nx==m:
                    continue
                if grid[i][j]+grid[ny][nx]==2:
                    ans=max(ans,dfs(ny,nx,dy,dx,not_use and dy==y and dx==x))
            ans+=1
            # self.log_vals(locals(),"i,j,y,x,use,ans")
            return ans
        ans=0
        for i in range(n):
            for j in range(m):
                if grid[i][j]!=1:
                    continue
                if ans==0:
                    ans=1
                for dy,dx in dr:
                    y,x=i+dy,j+dx
                    if y<0 or x<0 or y==n or x==m:
                        continue
                    if grid[y][x]==2:
                        ans=max(ans,dfs(y,x,dy,dx,True)+1)
        return ans


if __name__=='__main__':
    Solution().run()