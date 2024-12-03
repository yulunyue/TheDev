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
    from app.yly.algo.manage import SolutionBase
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
        self.add_value=0
        if l==r:
            self.value=self.arr[l]
        else:
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
        self.todo = 1

        
    def down(self):
        if self.todo:
            self.left.do(self.todo)
            self.right.do(self.todo)
            self.todo=0

    def up(self):
        self.value = self.r-self.l+1-self.value

class Solution(SolutionBase):
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
    
    def init(self,nums1: List[int], nums2: List[int], queries: List[List[int]]):
        SegTreeNode.arr=nums1
        self.n=len(nums1)
        self.ans=sum(nums2)
        self.root=SegTreeNode(0,self.n-1)
        self.queries=queries

    def execute(self, **kw) -> List[int]:
        result=[]
        for tp,a,b in self.queries:
            if tp==1:
                self.root.update(a,b,1)
            elif tp==2:
                self.ans+=self.root.query(0,self.n-1)*b
            else:
                result.append(self.ans)                
        return result
    def handleQuery(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
