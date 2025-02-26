from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
from common.algo.segtree import SegTreeNode
class T(SegTreeNode):
    def init(self):
        self.ct=0
    def do(self,v):
        self.ct+=v
        # self.todo+=v
        self.up()
    def up(self):
        if self.ct>0:
            self.value=self.r-self.l+1
        elif self.l==self.r:
            self.value=0
        else:
            self.value=self.left.value+self.right.value

class Solution(SolutionBase):
    _has_view=True
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
    
    def init(self, squares:list,*args, **kwargs):
        self.y_line=defaultdict(lambda:{-1:[],1:[]})
        self.mx,self.mn=-inf,inf
        for i,(x,y,c) in enumerate(squares):
            self.y_line[y+c][-1].append([x,x+c-1])
            self.y_line[y][1].append([x,x+c-1])
            self.mx=max(self.mx,x+c)
            self.mn=min(self.mn,x)
        self.yl=sorted(self.y_line.keys())
        self.t=T().set_range(self.mn,self.mx)
        return super().init(*args, **kwargs)
    
    def get_watch(self):
        return [
            View().add_node(
                View("log_str")
            ),
            View("t",size=6).graph()
        ]
    def execute(self,**kw):
        pre_y=self.mn
        ans=[]
        all_area=0
        for y in self.yl:
            w=self.t.query(self.mn,self.mx)
            if w:
                all_area+=(y-pre_y)*w
                ans.append([all_area,y,w])
            for tp in [-1,1]:
                for x1,x2 in self.y_line[y][tp]:
                    self.log('x1,x2,tp',locals())
                    self.t.update(x1,x2,tp)
                    w=self.t.query(self.mn,self.mx)
                    # self.log_vals(locals(),"y,x1,x2,tp,w","update")
            pre_y=y
        mid=ans[-1][0]/2
        i=bisect.bisect_left(ans,[mid])
        # self.log(ans)
        return ans[i][1]-(ans[i][0]-mid)/ans[i][-1]




if __name__=='__main__':
    Solution().run()