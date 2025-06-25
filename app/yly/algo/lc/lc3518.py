from common.util.export import logger, defaultdict
import math


class Solution:
    def get_cases(self):
        return [dict(s="abba", k=2, result="baab"), dict(s="kxk", k=2, result="")]

    def smallestPalindrome(self, s: str, k: int) -> str:
        n = len(s) // 2
        c = dict()
        for i in range(n):
            c[s[i]] = c.get(s[i], 0) + 1
        ks = sorted(c.keys())

        def calc():
            total = 0
            chen = 1
            for v in ks:
                if c[v] == 0:
                    continue
                total += c[v]
                chen *= math.comb(total, c[v])
            return chen

        l = []
        for i in range(n):
            for v in ks:
                if c[v] == 0:
                    continue
                c[v] -= 1
                p = calc()
                if p >= k:
                    l.append(v)
                    break
                k -= p
                c[v] += 1
        u = []
        if len(s) % 2 == 1:
            u = [s[len(s) // 2]]
        return "".join(l + u + l[::-1])
