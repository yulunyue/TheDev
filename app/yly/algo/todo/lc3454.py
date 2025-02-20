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
    
    def execute(self,squares:list):
        y_line=defaultdict(list)
        for i,(x,y,c) in enumerate(squares):
            y_line[y].append([x,x+c,0,i])
            y_line[y+c].append([x,x+c,1,i])
        for ly in sorted(y_line.keys()):
            self.log(ly,y_line[ly])




if __name__=='__main__':
    Solution().run()