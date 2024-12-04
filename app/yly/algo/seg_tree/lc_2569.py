from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from sortedcontainers import SortedList
from functools import lru_cache
import bisect
import sys
import math
import heapq
try:
    from app.yly.algo.manage import SolutionBase,WatchAny,Node
except:
    class SolutionBase:
        def log(self, *args, **kwargs):
            pass

        def run(self):
            pass
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7

class SegTreeNode(WatchAny):
    '''
                          1[0-6]
            2[0-3]                      3[4-6]
     4[0-1]        5[2-3]         6[4-5]         7[6-6]
8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    '''
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
        self.info = ""
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
    
    def update(self, l,r, value, info=""):
        self.info=info
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
        if v is None:
            self.todo += 1
        else:
            self.value = v

        
    def down(self):
        if self.todo:
            self.left.do(self.todo)
            self.right.do(self.todo)
            self.todo=0

    def up(self):
        self.value = self.left.value+self.right.value
    
    def to_node(self):
        ret = Node(title=f'id:{self.idx},v:{self.value},todo:{self.todo}').set_value(self.info)
        if self._left:
            ret.add_node(self._left.to_node())
        if self._right:
            ret.add_node(self._right.to_node())
        return ret
    
    def to_json(self):
        return self.to_node().set_type("graph").to_json()
    
    def hex_str(self):
        ret=f'{self.value}{self.todo}'
        if self._left:ret+=self._left.hex_str()
        if self._right:ret+=self._right.hex_str()
        return ret

class Solution(SolutionBase):
    _has_view=True
    def get_cases(self):
        return [
            dict(nums1=[1, 0, 1], nums2=[0, 0, 0], queries=[
                 [1, 1, 1], [2, 1, 0], [3, 0, 0]], result=[3]),
            dict(nums1=[0, 1, 0, 0, 0, 0],
                 nums2=[14, 4, 13, 13, 47, 18],
                 queries=[[3, 0, 0], [1, 4, 4], [1, 1, 4], [1, 3, 4], [3, 0, 0], [2, 5, 0], [
                     1, 1, 3], [2, 16, 0], [2, 10, 0], [3, 0, 0], [3, 0, 0], [2, 6, 0]],
                 result=[109, 109, 197, 197]),
       
        ]
    
    def init(self,nums1: List[int], nums2: List[int], queries: List[List[int]], result=0,**kwagrs):
        self.result=str(result)
        self.n=len(nums1)
        self.ans=sum(nums2)
        self.root=SegTreeNode(0,self.n-1)
        self.root.query(0,self.n-1)
        self._queries=queries
        self._nums1=nums1
        for i,v in enumerate(self._nums1):
            self.root.update(i,i,v,info=f'set {i} {v}')
    def execute(self, **kw) -> List[int]:
        result=[]
        for tp,a,b in self._queries:
            if tp==1:
                self.root.update(a,b,None)
            elif tp==2.1:
                self.ans+=self.root.query(0,self.n-1)*b
            elif tp==3.1:
                result.append(self.ans)                
        return result
    def handleQuery(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
