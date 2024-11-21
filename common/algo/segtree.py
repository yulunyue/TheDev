
from collections import defaultdict


class IntervalTreeNode:
    '''
                    16
        8
    4        12            20
  2   6   10    14     18
 1 3 5 7 9 11 13  15 17  19  21
    '''

    def __init__(self, size, default_value) -> None:
        self.array = [default_value]*size
        self.size = size

    def update_value(self, l, v):
        while l < self.size:
            self.array[l] = v(self.array[l])
            l += l & -l

    def query_value(self, l, f, init_value):
        ret = init_value
        while l > 0:
            ret = f(ret, self.array[l])
            l -= l & -l
        return ret

    def query_sum(self, l):
        return self.query_value(l, lambda a, b: a+b, 0)

    def add_value(self, l, v):
        self.update_value(l, lambda a: a+v)


class SegTreeNode:
    '''
                          1[0-6]
            2[0-3]                      3[4-6]
     4[0-1]        5[2-3]         6[4-5]         7[6-6]
8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    '''
    arr = []
    def __init__(self, l, r,idx=1, default_value=0) -> None:
        self.idx = idx
        self.l = l
        self.r = r
        self.m = (l+r)//2
        self.default_value = default_value
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
        self.down()
        res = 0
        if self.m < r:
            res+=self.right.query(l, r)
        if self.m >= l:
            res+=self.left.query(l, r)
        return res
    
    def update(self, l,r, value):
        if l <=self.l and self.r<= r:
            self.do(value)
            return
        self.down()
        if self.m < r:
            self.right.update(l, r,value)
        if self.m >= l:
            self.left.update(l, r,value)
        self.up()

    def do(self,v):
        self.do_sum(v)

    def do_sum(self,v):
        self.value +=(self.r-self.l+1)*v
        self.todo += v
        
    def down(self):
        if self.todo:
            self.left.do(self.todo)
            self.right.do(self.todo)
            self.todo=0

    def up(self):
        self.value = self.left.value+self.right.value

    def get_title(self):
        return "<br>".join([
            f"{self.idx}->[{self.l},{self.r}]:{SegTreeNode.arr[self.l:self.r+1]}" 
        ])


    def algo_view(self):
        ret = dict(
            title=self.get_title(),
            childs=[],
        )
        if self._left:
            ret['childs'].append(self._left.algo_view())
        if self._right:
            ret['childs'].append(self._right.algo_view())
        return ret
    
    def id_str(self):
        return f'{self.value}'
    
    def hex_str(self):
        ret = [self.id_str()]
        if self._left:
            ret.append(self._left.hex_str())
        if self._right:
            ret.append(self._right.hex_str())
        return "".join(ret)