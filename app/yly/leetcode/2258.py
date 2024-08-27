from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
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
            dict(grid = [[0,2,0,0,0,0,0],[0,0,0,2,2,1,0],[0,2,0,0,1,2,0],[0,0,2,2,2,0,2],[0,0,0,0,0,0,0]],result=3)
        ]
    def maximumMinutes(self, grid: List[List[int]]) -> int:
        n=len(grid)
        m=len(grid[0])
        dr = [[0,1],[0,-1],[1,0],[-1,0]]
        def get_next(y,x):
            ret=[]
            for ay,ax in dr:
                ny,nx=y+ay,x+ax
                if ny<0 or nx<0 or ny>=n or nx>=x:
                    continue
                ret.append([ny,nx])
            return ret

        fire_grass_time=dict()
        fire=[]
        for i,row in enumerate(grid):
            for j,cell in enumerate(row):
                if cell==1:
                    fire.append([0,i,j])
                    fire_grass_time[(i,j)]=0
                if cell==2:
                    fire_grass_time[(i,j)]=-1
        while fire:
            e_fire=fire
            fire=[]
            for t,i,j in e_fire:
                for y,x in get_next(i,j):
                    if (y,x) not in fire_grass_time:
                        fire_grass_time[(y,x)]=t+1
                        fire.append((t+1,y,x))
        q=[[0,0]]
        while q:
            tmp=q
            q=[]
            step=0
            for i,j in tmp:
                i,j=q.pop(0)
                if i==n and j==m:
                    if (i,j) not in fire_grass_time:
                        return 10**9
                    return
            step+=1 
        self.log(fire_grass_time)
        return -1


    def test(self, **kg):
        return self.maximumMinutes(**kg)

    def __init__(self, *args) -> None:
        self.local_debug = getattr(self, sys.argv[-1], None)
        if self.local_debug is None:
            print(sys.argv[-1], "not find")
    logs = ""

    def log(self, *s, tp: str = ""):
        if not self.local_debug or len(self.logs) >= 102400:
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
            self.ep = case.pop("result")
            try:
                r = self.local_debug(**case)
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r = None
            if not self.diff(r, self.ep):
                print(case, 'result', r, 'except', self.ep)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution().run()
