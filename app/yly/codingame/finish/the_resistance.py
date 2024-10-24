

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq
try:
    from app.yly.manage import SolutionBase
except:
    class SolutionBase:
        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass

        def run(self):
            l = input()
            n = int(input())
            ws = []
            for _ in range(n):
                ws.append(input())

            # Write an answer using print
            # To debug: print("Debug messages...", file=sys.stderr, flush=True)

            print(self.execute(l, ws))

inf = float("inf")


class Solution(SolutionBase):
    uri = '''https://www.codingame.com/ide/puzzle/the-resistance'''
    gameid = '597563014274696d6435ee1cc9b0d0dfcf82ba2b'
    CP = dict(
        A=".-", B="-...", C="-.-.", D="-..",
        E=".", F="..-.", G="--.", H="....",
        I="..", J=".---", K="-.-", L=".-..",
        M="--", N="-.", O="---", P=".--.",
        Q="--.-", R=".-.", S="...", T="-",
        U="..-", V="...-", W=".--", X="-..-",
        Y="-.--", Z="--..",
    )

    def get_cases(self):
        return [
            dict(s1="......-...-..---.-----.-..-..-..",
                 s2="HELL HELLO OWORLD WORLD TEST".split(' '), result=2),
            dict(s1="--.-------..",
                 s2="GOD GOOD MORNING G HELLO".split(' '), result=1),
            dict(s1='-.-', s2='A B C HELLO K WORLD'.split(' '), result=1)
        ]

    def execute(self, s1, s2):
        s2 = ["".join(self.CP[w] for w in word) for word in s2]
        n = len(s1)

        @lru_cache(None)
        def dfs(i):
            if i == n:
                return 1
            ans = 0
            for s in s2:
                if s == s1[i:i+len(s)]:
                    ans += dfs(i+len(s))
            return ans
        return dfs(0)


if __name__ == '__main__':
    Solution().run()
