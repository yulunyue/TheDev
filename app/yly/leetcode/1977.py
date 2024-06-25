from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product
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
            dict(num = '333',result=3),
            dict(num = "9999999999999",result=101),
            dict(num = "327",result=2),
            dict(num = "094",result=0),
        ]
    def numberOfCombinations(self, num: str) -> int:
        if num[0]=='0':
            return 0
        def small(a,b):
            # self.log('small',a,b)
            if len(a)<len(b):
                return True
            if len(a)>len(b):
                return False
            return a<b
        # @lru_cache(None)
        stack=[]
        def dfs(i,s):
            if i>=len(num):
                self.log(i,s,stack+[s])
                return 1
            
            ret=dfs(i+1,s+num[i])
            for j in range(i,len(num)):
                if small(num[i:j+1],s):
                    continue
                stack.append(s)
                ret+=dfs(j+1,num[i:j+1])
                stack.pop()
            return ret%M
        return dfs(1,num[0])
    def test(self, **kg):
        return self.numberOfCombinations(**kg)

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
                print(case, 'result',r, 'except',ep)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution().run()
