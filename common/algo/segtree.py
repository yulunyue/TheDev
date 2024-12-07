class SegTreeNode:
    '''
                          1[0-6]
            2[0-3]                      3[4-6]
     4[0-1]        5[2-3]         6[4-5]         7[6-6]
8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    '''
    FZ='FZ'
    QU='QU'
    def __init__(self, l, r,idx=1, default_value=0) -> None:
        self.idx = idx
        self.l = l
        self.r = r
        self.m = (l+r)//2
        self.default_value = default_value
        self.add_value=0
        self.value = default_value
        self.todo = 0
        self._left: SegTreeNode = None
        self._right: SegTreeNode = None
    
    @property
    def left(self):
        if not self._left:
            self._left = SegTreeNode(
                 self.l, self.m, self.idx*2,self.default_value)
        return self._left

    @property
    def right(self):
        if not self._right:
            self._right = SegTreeNode(
                self.m+1, self.r, self.idx*2+1, self.default_value)
        return self._right

    def query(self, l, r):
        if l <= self.l and self.r <= r:
            return self.value
        res = 0
        if self.m < r:
            res+=self.right.query(l, r)
        if self.m >= l:
            res+=self.left.query(l, r)
        return res
    
    def update(self, l,r, value):
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
        self.value = self.r-self.l+1-self.value
        if self.l!=self.r:
            self.todo=1-self.todo
        
    def down(self,v):
        if self.todo:
            self.left.do(v)
            self.right.do(v)
            self.todo = 1-self.todo
      
    def up(self,value):
        self.value = self.left.value+self.right.value
    
    def get_childs(self):
        ret = []
        if self._left:
            ret.append(self._left)
        if self._right:
            ret.append(self._right)
        return ret
    
    def get_title(self):
        return [
            bp("",self.idx,self.idx),
            bp('value', self.value,self.idx),
            bp('todo', self.todo,self.idx),
        ]
    
    def to_view(self):
        return dict(
            title=self.get_title(),
            childs=[v.to_view() for v in self.get_childs()]
        )

    def __str__(self):
        ret=f'{self.value}{self.todo}'
        if self._left:ret+=str(self._left)
        if self._right:ret+=str(self._right)
        return ret