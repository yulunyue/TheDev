from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
from common.algo.segtree import SegTreeNode
class T(SegTreeNode):
    def init(self):
        self.ct=0
    def do(self,v):
        self.ct+=v
        self.value=0 if self.ct==0 else (self.r-self.l+1)
        self.todo+=v
        SolutionBase().log_vals(self,'l,r,ct,value',"do")
    def up(self):
        SolutionBase().log_vals(self.left,'l,r,ct,value','up')
        SolutionBase().log_vals(self.right,'l,r,ct,value','up')
        self.value=self.left.value+self.right.value

class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/separate-squares-ii/description/'
    def get_cases(self):
        return [
            dict(squares = [[0,0,2],[1,1,2]],result=1.5),
            dict(squares = [[0,0,1],[2,2,1]],result=1.00000),
             
            dict(squares = [[0,0,2],[1,1,1]],result=1.00000)
        ]
    
    def separateSquares(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
    
    def execute(self,squares:list):
        y_line=defaultdict(lambda:{-1:[],1:[]})
        mx,mn=-inf,inf
        for i,(x,y,c) in enumerate(squares):
            y_line[y+c][-1].append([x,x+c-1])
            y_line[y][1].append([x,x+c-1])
            mx=max(mx,x+c)
            mn=min(mn,x)
        yl=sorted(y_line.keys())
        pre_y=mn
        ans=[]
        t=T().set_range(mn,mx)
        all_area=0
        for y in yl:
            w=t.query(mn,mx)
            if w:
                all_area+=(y-pre_y)*w
                ans.append([all_area,y,w])
            for tp in [-1,1]:
                for x1,x2 in y_line[y][tp]:
                    t.update(x1,x2,tp)
                    w=t.query(mn,mx)
                    self.log_vals(locals(),"y,x1,x2,tp,w","update")
            pre_y=y
        mid=ans[-1][0]/2
        i=bisect.bisect_left(ans,[mid])
        self.log(ans)
        return ans[i][1]-(ans[i][0]-mid)/ans[i][-1]




if __name__=='__main__':
    Solution().run()