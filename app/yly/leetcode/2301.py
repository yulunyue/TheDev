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
            dict(s = "fool3e7bar", sub = "leet", 
                 mappings = [["e","3"],["t","7"],["t","8"]],result=true),
        ]
    def matchReplacement(self, s: str, sub: str, mappings: List[List[str]]) -> bool:
        mp2:List[str,set]=dict()
        for f,t in mappings:
            if f not in mp2:
                mp2[f]={f}
            mp2[f].add(t)
        
        def dfs(l,r):
            if r>=len(sub):
                return True
            if l>=len(s):
                return False
            sr=mp2.get(sub[r],set({sub[r]}))
            if s[l] in sr:
                return dfs(l+1,r+1)
            return False

        for i,v in enumerate(s):
            if v in mp2.get(sub[0],set({sub[0]})):
                if dfs(i+1,1):
                    return True
        return False



    def test(self, **kg):
        return self.matchReplacement(**kg)

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
