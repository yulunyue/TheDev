inf=float("inf")
from typing import List
class SegTreeNode:
    '''
                          1[0-6]
            2[0-3]                      3[4-6]
     4[0-1]        5[2-3]         6[4-5]         7[6-6]
8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    '''
    QUERY_DEFAULT=None
    def __init__(self,idx=1) -> None:
        self.idx = idx
        self.todo = 0
        self.value = 0
        self._left: SegTreeNode = None
        self._right: SegTreeNode = None
    
    def get_value(self,*args):
        return self.value
    
    def do(self,v):
        pass
    def up(self,*args):
        pass
    def init(self):
        pass
    def set_range(self,l,r):
        self.l = l
        self.r = r
        self.m = (l+r)//2
        self.init()
        return self
    
    @property
    def left(self):
        if not self._left:
            self._left = self.__class__(
                 self.idx*2
            ).set_range(self.l, self.m)
        return self._left

    @property
    def right(self):
        if not self._right:
            self._right = self.__class__(
                self.idx*2+1,
            ).set_range(self.m+1, self.r)
        return self._right

    def query(self, l, r,fn=None):
        if l <= self.l and self.r <= r:
            return self.get_value()
        res = SegTreeNode.QUERY_DEFAULT
        self.down(self.todo)
        if self.m < r:
            res=fn(res,self.right.query(l, r,fn))
        if self.m >= l:
            res=fn(res,self.left.query(l, r, fn))
        return res

    def query_merge(self, l, r,*args):
        if l <= self.l and self.r <= r:
            return self.get_value(*args)
        if self.m < r:
            return self.right.query(l, r,*args)
        if self.m >= l:
            return self.left.query(l, r,*args)
        return self.up(*args)
    
    def build(self,nums):
        if self.l==self.r:
            self.do(nums[self.l])
            return
        self.left.build(nums)
        self.right.build(nums)
        self.up()
    
    
    def query_sum(self,l,r):
        return self.query(l,r,lambda a,b:a+b)
    
    def query_max(self, l, r):
        SegTreeNode.QUERY_DEFAULT = -inf
        return self.query(l,r,lambda a,b:a if a>b else b)

    def query_min(self, l, r):
        SegTreeNode.QUERY_DEFAULT = inf
        return self.query(l,r,lambda a,b:a if a<b else b)
        
    def update(self, l, r, value):
        if l <=self.l and self.r<= r:
            self.do(value)
            return
        self.down()
        if self.m >= l:
            self.left.update(l, r,value)
        if self.m < r:
            self.right.update(l, r,value)
        self.up()

    def down(self):
        if self.todo:
            self.left.do(self.todo)
            self.right.do(self.todo)
            self.todo = 0
      
    def get_childs(self):
        ret:List[SegTreeNode] = []
        if self._left:
            ret.append(self._left)
        if self._right:
            ret.append(self._right)
        return ret
    
    def get_data(self):
        from app.yly.algo.manage import bp
        key = f'seg_tree_{self.idx}'
        return [
            bp("",self.idx, key),
            bp('value', self.get_value()),
            bp('todo', self.todo,key),
        ]
    
    def tree_view(self):
        return dict(
            data=self.get_data(),
            childs=[v.tree_view() for v in self.get_childs()],
            key=f'seg_tree_{self.idx}',
        )
    
    def graph_view(self):
        return self.tree_view()

    def __str__(self):
        ret=f'{self.get_value()}{self.todo}'
        if self._left:ret+=str(self._left)
        if self._right:ret+=str(self._right)
        return ret