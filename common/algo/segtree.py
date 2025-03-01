from common.algo.manage import View,inf
from typing import List
class SegTreeNode(View):
    '''
                          1[0-6]
            2[0-3]                      3[4-6]
     4[0-1]        5[2-3]         6[4-5]         7[6-6]
8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    '''
    QUERY_DEFAULT=None
    VIEW_TYPE="graph"
    def __init__(self,idx=1) -> None:
        self.idx = idx
        self.todo = 0
        self.value = 0
        self._left: SegTreeNode = None
        self._right: SegTreeNode = None
    
    def do(self,v):
        pass

    def up(self,*args):
        pass


    def set_range(self,l,r):
        self.l = l
        self.r = r
        self.m = (l+r)//2
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
            return self.value
        res = SegTreeNode.QUERY_DEFAULT
        self.down()
        if self.m < r:
            res=fn(res,self.right.query(l, r,fn))
        if self.m >= l:
            res=fn(res,self.left.query(l, r, fn))
        return res

    
    def build(self,fn):
        if self.l==self.r:
            self.do(fn(self.l))
            return self
        self.left.build(fn)
        self.right.build(fn)
        self.up()
        return self
    
    
    def query_sum(self,l,r):
        SegTreeNode.QUERY_DEFAULT = 0
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
      

class FenNode(View):
    '''
                    16
        8
    4        12            20
  2   6   10    14     18
 1 3 5 7 9 11 13  15 17  19  21
    '''
    def set_range(self,size,default_value=0):
        self.size=(size+1)
        self.array = [default_value]*(size+1)
        return self
    
    def update(self, i, v):
        self.i = i+1
        while self.i < self.size:
            self.array[self.i] = v(self.array[self.i])
            self.i += self.i & -self.i
    
    def add(self,i,v):
        return self.update(i,lambda a:a+v)
 
    
    def query_value(self, i, f, init_value=0):
        ret = init_value
        self.i=i
        while self.i > 0:
            ret = f(ret, self.array[self.i])
            self.i &= self.i - 1
        return ret
    
    def query_sum(self, l,init_value=0):
        return self.query_value(l, lambda a, b: a+b, init_value)

    
