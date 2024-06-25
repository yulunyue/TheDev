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
            dict(nums = [5,-7,3,5], goal = 6,result=0)
        ]
    def minAbsDifference(self, nums: List[int], goal: int) -> int:
        n=len(nums)//2
        def help(m):
            mi=1<<len(m)
            st=set()
            for i in range(mi):
                tmp=0
                for j in range(i.bit_length()):
                    if i>>j&1:
                        tmp+=m[j]
                st.add(tmp)
            return sorted(list(st))
        a1=help(nums[0:len(nums)//2])
        a2=help(nums[len(nums)//2:])
        ret=inf
        self.log(a1,a2)
        for v in a1:
            idx=bisect.bisect_left(a2,goal-v)
            if idx<len(a2):
                ret=min(ret,abs(a2[idx]+v-goal))
            if idx>0:
                ret=min(ret,abs(a2[idx-1]+v-goal))
        return ret
    def test(self, **kg):
        return self.minAbsDifference(**kg)

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
