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
S1 = 'xwxlxktiyjapmuqiezqqhqaieceiceetfpytqopmwjmtlbkzysihppbdqgtupqcgwzhbjriwbuwnekgspidlyhholgwhjsdspyufffrutkgnmtyrnikueahyefjtljstoynlwdnsmvlsjnmexeritzdividztirexemnjslvmsndwlnyotsjltjfeyhaeukinrytmngkturfffuypsdsjhwglohhyldipsgkenwubwirjbhzwgcqputgqdbpphisyzkbltmjwmpoqtypfteecieceiaqhqqzeiqumpajyitkxlxwx'


class Solution:
    def get_cases(self):
        return [
            dict(s="wtbptdhbjqsrwkxccxkwrsqjbhdtpbtw", result=1),
            dict(s=S1, result=1245),
            dict(s="ababbb", result=9)
        ]

    def maxProduct(self, s: str) -> int:

        @lru_cache(None)
        def dfs(a, b):
            if a > b:
                return False, 0
            if a == b:
                return True, 1
            if s[a] == s[b]:
                is_huiwen, num = dfs(a+1, b-1)
                if is_huiwen:
                    # self.log(a, b, s[a:b+1], 2+num)
                    return is_huiwen, 2+num
                return is_huiwen, num
            _, rn = dfs(a+1, b)
            _, ln = dfs(a, b-1)
            return False, max(rn, ln)
        ret = 1
        for i in range(0, len(s)-1):
            a = dfs(0, i)
            b = dfs(i+1, len(s)-1)
            if a[1]*b[1] > ret:
                self.log(a, i, b)
                ret = max(ret, a[1]*b[1])
        return ret

    def test(self, **kg):
        return self.maxProduct(**kg)

    def __init__(self, *args) -> None:
        self.local_debug = getattr(self, sys.argv[-1], None)
        if self.local_debug is None:
            print(sys.argv[-1], "not find")
    logs = ""

    def log(self, *s, tp: str = ""):
        if not self.local_debug or len(self.logs) >= 204800:
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
                print(case, r, ep)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution().run()
