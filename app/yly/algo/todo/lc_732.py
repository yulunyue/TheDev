from app.yly.algo.manage import SolutionBase,View
from common.algo.segtree import SegTreeNode
from sortedcontainers import SortedList
from typing import Dict,List
from collections import defaultdict
from functools import lru_cache
import bisect
MOD=(10**9)+7
inf = float("inf")
false=False
true=True
null=None
class St(SegTreeNode):
    def do(self, v):
        self.todo+=v
        self.value+=v
    
    def up(self, value):
        self.value=max(self.left.value,self.right.value)

class MyCalendarThree(SolutionBase):
    uri='lc_cls'
    def get_watch(self):
        return [
      
        ]
    def get_cases(self):
        return [dict(
            mathods=["MyCalendarThree","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book"],
            params=[[],[47,50],[1,10],[27,36],[40,47],[20,27],[15,23],[10,18],[27,36],[17,25],[8,17],[24,33],[23,28],[21,27],[47,50],[14,21],[26,32],[16,21],[2,7],[24,33],[6,13],[44,50],[33,39],[30,36],[6,15],[21,27],[49,50],[38,45],[4,12],[46,50],[13,21]],
            result=[null,1,1,1,1,1,2,2,2,3,3,3,4,5,5,5,5,5,5,6,6,6,6,6,6,7,7,7,7,7,7])]
    

    def __init__(self):
        self.init()

    def init(self, *args, **kwargs):
        self.array=SortedList()
        self.ct=defaultdict(int)
        return super().init(*args, **kwargs)


    def book(self, startTime: int, endTime: int) -> int:
        if startTime not in self.ct:
            self.array.add(startTime)
        if endTime not in self.ct:
            self.array.add(endTime)
        self.ct[startTime]+=1
        self.ct[endTime]-=1
        ret=-inf
        ans=0
        for v in self.array:
            ans+=self.ct[v]
            ret=max(ans,ret)
        return ret

# Your MyCalendarThree object will be instantiated and called as such:
# obj = MyCalendarThree()
# param_1 = obj.book(startTime,endTime)

if __name__=='__main__':
    MyCalendarThree().run()