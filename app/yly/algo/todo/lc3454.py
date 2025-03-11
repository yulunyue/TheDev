from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
from common.algo.segtree import SegTreeNode
class T(SegTreeNode):
    ct=0
    def do(self,v):
        self.ct+=v
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
        xs=[]
        self.events=[]
        for lx,y,l in squares:
            rx=lx+l
            xs.append(lx)
            xs.append(rx)
            self.events.append(y,lx,rx,1)
            self.events.append(y+l,lx,rx,-1)
        self.xs=sorted(set(xs))
        self.x_id=dict()
        for i,x in enumerate(self.xs):
            self.x_id[x]=i
        self.t=T().set_range(0,len(xs)-1)
        self.events.sort()

    def get_view(self):
        return View(
            View(
                View(key="log_str")
            ),
            View(key="t")
        )
    
    def execute(self,**kw):
        records=[]
        tot_area=0
        for i in range(1,len(self.events)):
            y,lx,rx,delta=self.events[i-1]
            l,r=self.x_id[lx],self.x_id[rx]
            self.t.update(l,r,delta)
            s=self.xs[-1]-self.xs[0]-self.t.get_uncover()
            records.append(tot_area)
            tot_area+=s*(self.events[i]-y)




if __name__=='__main__':
    Solution().run()