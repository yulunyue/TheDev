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
            dict(k = 2, n = 5,result=25),
        ]   
    def kMirror(self, k: int, n: int) -> int:
        l,r=1,10
        cnt=0
        def check(v):
            ret=[]
            ret1=[]
            while v>0:
                v,c=v//k,v%k
                ret.append(c)
                ret1.insert(0,c)
            return ret==ret1
        ans=0
        while 1:
            for op in [0,1]:
                for v in range(l,r):
                    b=1
                    s=0
                    if op==0:
                        a=v//10
                    else:
                        a=v
                    while v>0:
                        v,c=v//10,v%10
                        s=s*10+c
                        b*=10
                    if check(a*b+s):
                        ans+=a*b+s
                        cnt+=1      
                        if cnt==n:
                            return ans        
            l,r=r,r*10


    def test(self, **kg):
        return self.kMirror(**kg)

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
