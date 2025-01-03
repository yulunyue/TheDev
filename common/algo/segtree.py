inf=float("inf")
class SegTreeNode:
    '''
                          1[0-6]
            2[0-3]                      3[4-6]
     4[0-1]        5[2-3]         6[4-5]         7[6-6]
8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    '''

    def __init__(self,idx=1, default_value=0) -> None:
        self.idx = idx
        self.default_value = default_value
        self.value = default_value
        self.todo = 0
        self._left: SegTreeNode = None
        self._right: SegTreeNode = None
    
    def set_range(self,l,r):
        self.l = l
        self.r = r
        self.m = (l+r)//2
        return self
    
    @property
    def left(self):
        if not self._left:
            self._left = self.__class__(
                 self.idx*2,self.default_value
            ).set_range(self.l, self.m)
        return self._left

    @property
    def right(self):
        if not self._right:
            self._right = self.__class__(
                self.idx*2+1, self.default_value
            ).set_range(self.m+1, self.r)
        return self._right

    def query_sum(self, l, r):
        if l <= self.l and self.r <= r:
            return self.value
        res = 0
        if self.m < r:
            res+=self.right.query_sum(l, r)
        if self.m >= l:
            res+=self.left.query_sum(l, r)
        return res
    
    def query_max(self, l, r):
        if l <= self.l and self.r <= r:
            return self.value
        res = -inf
        self.down(self.todo)
        if self.m < r:
            res=max(res,self.right.query_max(l, r))
        if self.m >= l:
            res=max(res,self.left.query_max(l, r))
        return res

        
    def update(self, l, r, value):
        if l <=self.l and self.r<= r:
            self.do(value)
            return self.value
        self.down(value)
        if self.m >= l:
            self.left.update(l, r,value)
        if self.m < r:
            self.right.update(l, r,value)
        self.up(value)
        return self.value

    def do(self,v):
        pass

    def update_value(self,v):
        pass
        
    def down(self,v):
        if self.todo:
            self.left.do(v)
            self.right.do(v)
            self.todo = 0
      
    def up(self,value):
        pass
    
    def get_childs(self):
        ret = []
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
            bp('value', self.value,key),
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
        ret=f'{self.value}{self.todo}'
        if self._left:ret+=str(self._left)
        if self._right:ret+=str(self._right)
        return ret