from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product
from sortedcontainers import SortedList
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7


class Solution:
    def get_cases(self):
        return [
            dict(tasks =[5,4],workers =[0,0,0],pills =1,strength =5,result=1),
            dict(tasks =[5,9,8,5,9],workers =[1,6,4,2,6],pills=1,strength =5,result=3),
            dict(tasks =[10,15,30],workers =[0,10,10,10,10],pills =3,strength=10,result=2),
            dict(tasks = [3,2,1], workers = [0,3,3], pills = 1, strength = 1,result=3)
        ]
    def maxTaskAssign(self, tasks: List[int], workers: List[int], pills: int, strength: int) -> int:
        tasks.sort()
        workers=[[v,0] for v in workers]
        # workers.sort()
        heapq.heapify(workers)
        ret=0
        while workers and tasks:
            # self.log(workers,tasks)
            w,flag=heapq.heappop(workers)
            if pills<=0 and flag==1:
                continue
            if w>=tasks[0]:
                if flag==1:
                    pills-=1
                ret+=1
                tasks.pop(0)
                continue
            if flag==0:
                heapq.heappush(workers,[w+strength,1])
           
        return ret
            

    

    def test(self, **kg):
        return self.maxTaskAssign(**kg)

    def __init__(self, *args) -> None:
        self.local_debug = getattr(self, sys.argv[-1], None)
        if self.local_debug is None:
            print(sys.argv[-1], "not find")
    logs = ""

    def log(self, *s, tp: str = ""):
        if not self.local_debug or len(self.logs) >= 2048:
            return
        if tp:
            self.draw(s[0], tp)
        self.logs += " ".join([str(v) for v in s])+"\n"

    def draw(self, s, tp: str):
        from common.tool.draw import Draw
        d = Draw()
        if tp.startswith('bar'):
            d.draw_bar_chart(s)
        elif tp.startswith('graph'):
            d.draw_graph(s)
        d.save(f"data/log/{tp}.png")

    def run(self):
        if not self.local_debug:
            return
        for case in self.get_cases():
            self.logs = ""
            ep = case.pop("result")
            try:
                r = self.local_debug(**case)
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r = None
            if not self.diff(r, ep):
                print(case, 'result', r, 'except', ep)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution().run()
