from typing import List
from common.util.export import logger
import bisect
import math


class Solution:
    def get_cases(self):
        return [dict(nums=[2, 4, 9, 6], maxC=1, result=2)]

    def minStable(self, nums: List[int], maxC: int) -> int:
        def check(upper: int):
            intervals = []
            left = maxC
            for i, x in enumerate(nums):
                for p in intervals:
                    p[0] = math.gcd(p[0], x)
                intervals.append([x, i])
                idx = 1
                for j in range(1, len(intervals)):
                    if intervals[j][0] != intervals[j - 1][0]:
                        intervals[idx] = intervals[j]
                        idx += 1
            del intervals[idx]
            if intervals[0][0] == 1:
                intervals.pop(0)
            if intervals and i - intervals[0][1] + 1 > upper:
                if left == 0:
                    return False
                left -= 1
                intervals.clear()
            return True

        u = len(nums) // (maxC + 1)
        return bisect.bisect_left(range(u), True, key=check)
