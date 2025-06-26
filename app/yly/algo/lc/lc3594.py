from typing import List
from common.util.export import logger, functools, C, math, heapq, defaultdict


class Solution:
    def get_cases(self):
        return [dict(n=3, k=2, m=3, time=[2, 5, 8], mul=[1.0, 1.5, 0.75], result=14.5)]

    def minTime(
        self, n: int, k: int, m: int, time: List[int], mul: List[float]
    ) -> float:
        mask = (1 << n) - 1
        time.sort()
        tc = defaultdict(list)
        for i in range(mask + 1):
            j = i
            while j:
                if j.bit_count() <= k:
                    tc[mask - i].append([mask - (j ^ i), time[j.bit_length() - 1]])
                j = (j - 1) & i

        # logger.map(tc=dict(tc), mask=mask)
        ct = defaultdict(lambda: C.inf)
        h = [(0, 0, 0, 0)]
        self.ans = C.inf

        def put(s, t, tm, mi, lr):
            tadd = tm * mul[mi]
            mi = (mi + math.floor(tadd)) % m
            t += tadd
            key = s, mi, lr
            if t < ct[key]:
                ct[key] = t
                if s == mask and lr == 1:
                    self.ans = t
                heapq.heappush(h, [t, s, mi, lr])

        while h:
            t, s, mi, lr = heapq.heappop(h)
            # logger.map(s=f"{s:03b}", t=t, mi=mul[mi], lr=lr)
            if lr == 0:
                for s2, tm in tc[s]:
                    put(s2, t, tm, mi, 1)
            else:
                j = s
                while j:
                    low_bit = j & -j
                    put(s - low_bit, t, time[low_bit.bit_length() - 1], mi, 0)
                    j -= low_bit

        return -1 if self.ans == C.inf else self.ans
