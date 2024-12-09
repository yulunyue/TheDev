from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from sortedcontainers import SortedList
from functools import lru_cache
import bisect
import sys
import math
import heapq
from app.yly.algo.manage import SolutionBase,View,bp

inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7



class Solution(SolutionBase):
    _has_view=True
    action="log"
    uid="https://leetcode.cn/problems/handling-sum-queries-after-update/description/"
    def get_cases(self):
        return [
            dict(nums1 =[1,0,1],nums2 =[44,28,35],queries =[[1,0,1],[2,10,0],[2,2,0],[2,7,0],[3,0,0],[3,0,0],[1,2,2],[1,1,2],[2,1,0],[1,0,2],[1,2,2],[1,0,2],[3,0,0],[1,1,2],[3,0,0],[1,0,1],[2,21,0],[1,0,1],[2,26,0],[1,1,1]],result=[145,145,146,146]),
            dict(nums1=[1, 0, 1], nums2=[0, 0, 0], queries=[
                 [1, 1, 1], [2, 1, 0], [3, 0, 0]], result=[3]),
            dict(nums1=[0, 1, 0, 0, 0, 0],
                 nums2=[14, 4, 13, 13, 47, 18],
                 queries=[[3, 0, 0], [1, 4, 4], [1, 1, 4], [1, 3, 4], [3, 0, 0], [2, 5, 0], [
                     1, 1, 3], [2, 16, 0], [2, 10, 0], [3, 0, 0], [3, 0, 0], [2, 6, 0]],
                 result=[109, 109, 197, 197]),
       
        ]
    
    def init(self,nums1: List[int], nums2: List[int], queries: List[List[int]], result=0,**kwagrs):
        self.ans=result
        self._n=len(nums1)
        self.sum=sum(nums2)
        self.result=[]
        self.root=SegTreeNode(0,self._n-1)
        self.root.query(0,self._n-1)
        self._queries=queries
        self.nums1=nums1
        for i,v in enumerate(self.nums1):
            if v==0:
                continue
            self.root.update(i,i,SegTreeNode.FZ)
    
    def get_watch(self):
        return View().add_node(
            View().add_node(
                View(key="nums1"),
                View(key="ans"),
                View(key="result"),
                View(key="sum"),
                View(key="action"),
            ),
            View(key="root",size=30).tree(),
        )
    
    def execute(self,*args,**kw) -> List[int]:
        for tp,a,b in self._queries:
            if tp==1:
                self.log(f'update {a} {b}')
                self.root.update(a,b,SegTreeNode.FZ)
            elif tp==2:
                self.log(f'query *{a}')
                self.sum+=self.root.query(0,self._n-1)*a
            elif tp==3:
                self.log(f'sum')
                self.result.append(self.sum)                
        return self.result
    
    def handleQuery(self, *args, **kg):
        self.init(*args,**kg)
        return self.execute(*args, **kg)



if __name__ == '__main__':
    Solution().run()
