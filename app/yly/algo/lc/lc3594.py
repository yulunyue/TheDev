from typing import List
from common.util.export import logger, functools, C, math, heapq, defaultdict
from common.algo.base.graph import Graph


class Solution:
    def get_cases(self):
        return [dict(n=3, k=2, m=3, time=[2, 5, 8], mul=[1.0, 1.5, 0.75], result=14.5)]

    def minTime(
        self, n: int, k: int, m: int, time: List[int], mul: List[float]
    ) -> float:
        mask = (1 << n) - 1
        ss = defaultdict(list)
        max_t = dict()
        for i in range(1, mask + 1):
            if i.bit_count() > m:
                continue
            j = i
            ss[j] = []
            max_t[i]
            while i:
                low_bit = i & -i
                ss[j].append(low_bit.bit_length() - 1)
                i -= low_bit
                max_t
        h = [[0, 0, 0, 0]]
        while h:
            t, s1, s2, lr = heapq.heappop(h)
