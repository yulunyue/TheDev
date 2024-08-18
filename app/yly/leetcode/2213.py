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


class SegTree:
    '''
                          1[0-6]
            2[0-3]                      3[4-6]
     4[0-1]        5[2-3]         6[4-5]         7[6-6]
8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    '''

    def __init__(self, size, default_value=None) -> None:
        self.size = size
        self.default_value = float(
            "inf") if default_value is None else default_value
        self.init()

    def init(self):
        self.pre = [self.default_value]*(self.size*4)
        self.suf = [self.default_value]*(self.size*4)
        self.mux = [self.default_value]*(self.size*4)

    def build(self, o, l, r, s):
        if l == r:
            self.pre[o] = self.suf[o] = self.mux[o] = 1
            return
        m = (l+r)//2
        self.build(o*2, l, m, s)
        self.build(o*2+1, m+1, r, s)
        self.merge(o, m, s)

    def update_one(self, o, l, r, i, s):
        if l == r:
            return
        m = (l+r)//2
        if i <= m:
            self.update_one(o*2, l, m, i, s)
        else:
            self.update_one(o*2+1, m+1, r, i, s)
        self.merge(o, m, s)

    def merge(self, o, m, s):
        self.pre[o] = self.pre[o*2]
        self.suf[o] = self.suf[o*2+1]
        self.mux[o] = max(self.mux[o*2], self.mux[o*2+1])
        if s[m-1] == s[m]:
            if self.pre[o*2] == self.suf[o*2]:
                self.pre[o*2] += self.pre[o*2+1]
            if self.pre[o*2+1] == self.suf[o*2+1]:
                self.suf[o*2+1] += self.suf[o*2]
            self.mux[o] = max(self.mux[o], self.suf[o*2]+self.pre[o*2+1])


class Solution:
    def get_cases(self):
        return [
            dict(s="geuqjmt", queryCharacters="bgemoegklm", queryIndices=[3, 4, 2, 6, 5, 6, 5, 4, 3, 2],
                 result=[1, 1, 2, 2, 2, 2, 2, 2, 2, 1]),
            dict(s="babacc", queryCharacters="bcb",
                 queryIndices=[1, 3, 3], result=[3, 3, 4])
        ]

    def longestRepeating(self, s: str, queryCharacters: str, queryIndices: List[int]) -> List[int]:
        n = len(s)
        s = list(s)
        st = SegTree(n, default_value=0)
        st.build(1, 1, n, s)
        ret = []
        for i, idx in enumerate(queryIndices):
            s[idx] = queryCharacters[i]
            st.update_one(1, 1, n, idx+1, s)
            ret.append(st.mux[1])
        return ret

    def test(self, **kg):
        return self.longestRepeating(**kg)

    def __init__(self, *args) -> None:
        self.local_debug = getattr(self, sys.argv[-1], None) or 1
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
