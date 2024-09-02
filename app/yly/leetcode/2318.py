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

MOD, MX = 10 ** 9 + 7, 10 ** 4 + 1
f = [[0] * 6 for _ in range(MX + 1)]
f[1] = [1] * 6
for i in range(2, MX):
    for j in range(6):
        for k in range(6):
            if k != j and math.gcd(k + 1, j + 1) == 1:
                f[i][j] += f[i - 1][k] - f[i - 2][j]
        if i > 3:
            f[i][j] += f[i - 2][j]
        f[i][j] %= MOD


class Solution:
    def distinctSequences(self, n: int) -> int:
        return sum(f[n]) % MOD


class Solution:
    def get_cases(self):
        return [
            dict(n=4, result=184),
            dict(n=10**4, result=1.1),
        ]

    def distinctSequences(self, n):
        if n == 1:
            return 6

        n2 = defaultdict(list)
        for i in range(1, 7):
            for j in range(1, 7):
                if math.gcd(i, j) != 1 or i == j:
                    continue
                for k in range(1, 7):
                    if k != i and math.gcd(j, k) == 1 and k != i and k != j:
                        n2[i, j].append(k)
        if n == 2:
            return len(n2.keys())

        @lru_cache(None)
        def dfs(cur, n):
            if n == 1:
                return len(n2[cur])
            ret = 0
            for s in n2[cur]:
                ret += dfs((cur[1], s), n-1)
            return ret % M

        # def dfs(cur, n):
        #     if n == 1:
        #         return len(n2[cur])
        #     ret = 0
        #     stack = [(cur, n)]
        #     while stack:
        #         cur, n = stack.pop()
        #         if n == 1:
        #             ret += len(n2[cur])
        #         else:
        #             for s in n2[cur]:
        #                 stack.append(((cur[1], s), n-1))
        #     return ret % M
        ans = sum(dfs(cu, n-2) for cu in n2) % M
        return ans

    def test(self, **kg):
        return self.distinctSequences(**kg)

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
