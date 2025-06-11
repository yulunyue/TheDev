from typing import List
import bisect
from common.algo.base.lazyheap import LazyHeapMinMax


class Solution:
    def get_cases(self):
        return [
            dict(nums=[1, 2], k=1, x=2, result=1),
            dict(nums=[3, 2, 4, 7, 1, 5, 4], k=2, x=3, result=6),
            dict(nums=[5, -2, 1, 3, 7, 3, 6, 4, -1], x=3, k=2, result=8),
        ]

    def minOperations(self, nums: List[int], x=int, k=int):
        """
        中位数定理 一个区间的最小代价为这个区间所有数到中位数的具体
        """
        h = LazyHeapMinMax()
        rsize = x // 2
        lsize = x - rsize
        s = []
        for i, v in enumerate(nums):
            h.pushpop(v)
            if i >= x - 1:
                lsum = h.left_max_heap.top() * lsize - h.left_max_heap.get_sum()
                rsum = h.right_min_heap.get_sum() - h.left_max_heap.top() * rsize
                s.append(lsum + rsum)
                h.remove(nums[i - x + 1])
        inf = float("inf")
        n = len(nums)
        r = [[0] * (n + 1) for _ in range(k + 1)]
        for i in range(1, k + 1):
            r[i][i * x - 1] = inf
            for j in range(i * x, n - (k - i) * x + 1):
                r[i][j] = min(r[i][j - 1], r[i - 1][j - x] + s[j - x])
        return r[k][n]
