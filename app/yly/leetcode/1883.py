from typing import List,Dict,Optional
from collections import defaultdict, deque,Counter
from itertools import accumulate,product
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf=float("inf")
null=None
true=True
false=False
M=10**9 + 7


class Solution:
    def get_cases(self):
        return [
            dict(dist = [7,3,5,5], speed = 1, hoursBefore = 10, result=-1),
            dict(dist = [7,3,5,5], speed = 2, hoursBefore = 10, result=2),
            dict(dist = [1,3,2], speed = 4, hoursBefore = 2, result=1),
        ]
    def minSkips(self, dist: List[int], speed: int, hoursBefore: int) -> int:
        pass

    
    def test(self,**kw):
        return self.minSkips(**kw)

    def init(self,*args):
        pass

    def __init__(self,*args) -> None:
        self.local_debug=getattr(self,sys.argv[-1],None)
        self.init(*args)
        if self.local_debug is None:
            print(sys.argv[-1],"not find")
    logs = ""
    def log(self, *s,tp:str=""):
        if not self.local_debug or len(self.logs)>=2048:
            return
        if tp:
            self.draw(s[0],tp)
        self.logs += " ".join([str(v) for v in s])+"\n"
    def draw(self,s,tp:str):
        from common.tool.draw import Draw
        d=Draw()
        if tp.startswith('bar'):
            d.draw_bar_chart(s)
        elif tp.startswith('graph'):
            d.draw_graph(s)
        d.save(f"data/log/{tp}.png")
    
    def run(self):
        if not self.local_debug:
            return
        for case in self.get_cases():
            self.logs=""
            ep=case.pop('result')
            try:
                r=self.local_debug(**case)
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r=None
            if not self.diff(r,ep):
                print(case,f'r:{r},result:{ep}')
                print(self.logs)
                break
            
    def diff(self,a,b):
        if isinstance(a,float) and isinstance(b,float):
            return "%.2f"%(a)=="%.2f"%(b)
        return a==b

    



      

if __name__ == '__main__':
    Solution().run()



