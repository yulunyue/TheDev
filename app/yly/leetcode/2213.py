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
            dict(s="geuqjmt", queryCharacters="bgemoegklm", queryIndices=[3, 4, 2, 6, 5, 6, 5, 4, 3, 2],
                 result=[1, 1, 2, 2, 2, 2, 2, 2, 2, 1]),
            dict(s="babacc", queryCharacters="bcb",
                 queryIndices=[1, 3, 3], result=[3, 3, 4])
        ]

    def longestRepeating(self, s: str, queryCharacters: str, queryIndices: List[int]) -> List[int]:
        s = list(s)+['?']
        sl = SortedList()
        pos = [0]
        j = 0
        for i in range(1, len(s)):
            if s[i] != s[i-1]:
                pos.append(i)
                sl.add(i-j)
                j = i
        ret = []
        self.log("".join(s), pos, sl)
        for i, idx in enumerate(queryIndices):

            if s[idx] != queryCharacters[i]:

                flag1 = idx > 0 and queryCharacters[i] == s[idx-1]
                flag2 = queryCharacters[i] == s[idx+1]
                if flag1 and flag2:
                    j = bisect.bisect_left(pos, idx)
                    sl.remove(pos.pop(j+1)-pos[j])
                    sl.remove(pos.pop(j)-pos[j-1])
                    sl.add(pos[j]-pos[j-1])
                elif flag2:
                    j = bisect.bisect_left(pos, idx+1)
                    sl.remove(pos.pop(j)-pos[j-1])
                    sl.add(pos[j]-pos[j-1])

                elif flag1:
                    j = bisect.bisect_left(pos, idx)
                    sl.remove(pos[j]-pos[j-1])
                    if pos[j]+1 == pos[j+1]:
                        pos.pop(j)
                    else:
                        pos[j] += 1
                    sl.add(pos[j]-pos[j-1])
                else:
                    if idx == 0:
                        idx = 1
                    j = bisect.bisect_left(pos, idx)
                    if pos[j] != idx:
                        sl.remove(pos[j]-pos[j-1])
                        pos.insert(j, idx)
                        sl.add(pos[j]-pos[j-1])
                        sl.add(pos[j+1]-pos[j])
                s[idx] = queryCharacters[i]
                self.log(idx, "".join(s), pos, sl, flag1, flag2)

            ret.append(sl[-1])
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
