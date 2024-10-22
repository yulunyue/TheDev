from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from sortedcontainers import SortedList
from functools import lru_cache
import bisect
import sys
import math
import heapq
try:
    from app.yly.leetcode.manage import SolutionBase
except:
    class SolutionBase:
        def log(self, *args, **kwargs):
            pass

        def run(self):
            pass
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7


def kmp_next(l, s, pi, v):
    while l and s[l] != v:
        l = pi[l-1]
    if s[l] == v:
        l += 1
    return l


def kmp_array(s):
    '''
    ret[i]= max(j->[1,n] => s[:j]==s[-j:]))
    '''
    n = len(s)
    pi = [0]*n
    l = 0
    for r in range(1, n):
        l = kmp_next(l, s, pi, s[r])
        pi[r] = l
    return pi


def kmp_search(src, target):
    pi = kmp_array(target)
    m = len(target)
    mathch_idx = []
    c = 0
    for i, v in enumerate(src):
        c = kmp_next(c, target, pi, v)
        if c == len(target):
            mathch_idx.append(i-m+1)
            c = pi[c-1]
    return mathch_idx


class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(target="abcdef", words=["abdef", "abc", "d", "def", "ef"], costs=[
                 100, 1, 1, 10, 5], result=7)
        ]

    def execute(self, target: str, words: List[str], costs: List[int]) -> int:
        n = len(target)
        g = [[] for _ in range(n+1)]
        for i, word in enumerate(words):
            idx = kmp_search(target, word)
            for nid in idx:
                g[nid].append([nid+len(word), costs[i]])
        start = 0
        dist = defaultdict(lambda: float('inf'))
        dist[start] = 0
        q = [(0, start)]
        while q:
            cost, u = heapq.heappop(q)
            # self.log(u, cost)
            if u == n:
                return cost
            if cost > dist[u]:
                continue
            for v, weight in g[u]:
                target = cost + weight
                if target < dist[v]:
                    dist[v] = target
                    heapq.heappush(q, (dist[v], v))
        return -1

    def minimumCost(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
