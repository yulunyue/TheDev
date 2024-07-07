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
            dict(s1 = "internationalization", s2 = "i18n",result=true),
            dict(s1 = "112s", s2 = "g841",result=true),
            
        ]
    @lru_cache(None)
    def comb(self,s):
        s=[int(v) for v in s]
        ret=[s[-1]]
        chen=[1]
        for i in range(len(s)-2,-1,-1):
            chen.append(chen[-1]*10)
            tmp=ret
            ret=[]
            for c in chen:
                for d in tmp:
                    ret.append(c*s[i]+d)
            self.log(ret)
        return ret
    def tointarray(self,s:str):
        ret=[]
        int_v=""
        for v in s:
            if v.isdigit():
                int_v+=v
                continue
            if int_v:
                ret.append(self.comb(int_v))
                int_v=""
            ret.append(v)
        if int_v:
            ret.append(self.comb(int_v))
        return ret
    def possiblyEquals(self, s1: str, s2: str) -> bool:
        # s1=self.tointarray(s1)
        # s2=self.tointarray(s2)
        def dfs(i1,i2,cha):
            pass
        self.log(self.comb("123"))
        return dfs(0,0,0)

    def test(self, **kg):
        return self.possiblyEquals(**kg)

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
