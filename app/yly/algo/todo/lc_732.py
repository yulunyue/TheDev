from app.yly.algo.manage import SolutionBase,View
from common.algo.segtree import SegTreeNode
from typing import Dict,List
from functools import lru_cache
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
    _has_view = True
    def get_watch(self):
        return [
            View("seg").graph()
        ]
    def get_cases(self):
        return [dict(
            mathods=["MyCalendarThree","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book"],
            params=[[],[47,50],[1,10],[27,36],[40,47],[20,27],[15,23],[10,18],[27,36],[17,25],[8,17],[24,33],[23,28],[21,27],[47,50],[14,21],[26,32],[16,21],[2,7],[24,33],[6,13],[44,50],[33,39],[30,36],[6,15],[21,27],[49,50],[38,45],[4,12],[46,50],[13,21]],
            result=[null,1,1,1,1,1,2,2,2,3,3,3,4,5,5,5,5,5,5,6,6,6,6,6,6,7,7,7,7,7,7])]
    

    def __init__(self):
        self.init()

    def init(self,params=None,**kwargs):
        self.seg=St().set_range(0,MOD)     

    def book(self, startTime: int, endTime: int) -> int:
        self.seg.update(startTime,endTime-1,1)
        return self.seg.value

# Your MyCalendarThree object will be instantiated and called as such:
# obj = MyCalendarThree()
# param_1 = obj.book(startTime,endTime)

if __name__=='__main__':
    MyCalendarThree().run()