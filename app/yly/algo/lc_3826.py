from common.util.export import (
    List,
    MockCf,
    functools,
    CT,
    bisect,
    heapq,
    itertools,
    deque,
)
from common.algo.base.geo.vec import Vec


class Solution(MockCf):
    def get_cases(self):
        """ """
        return dict(
            case0=dict(nums=[1, 1, 1], k=3, result=3),
            case1=dict(nums=[1, 1, 1], k=2, result=4),
            case2=dict(nums=[13, 8, 19], k=2, result=421),
            case3=dict(nums=[5, 1, 2, 1], k=2, result=25),
            case4=dict(nums=[36, 39, 33], k=2, result=3294),
            case5=dict(nums=[3, 11, 24, 35, 8, 2], k=5, result=1057),
            case6=dict(nums=[30, 21, 30, 45], k=2, result=4176),
        )

    def minPartitionScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        pre = list(itertools.accumulate(nums, initial=0))
        f = [0] + [CT.inf] * n
        for K in range(1, k + 1):
            s = pre[K - 1]
            p = Vec(-2 * s, 1)

    execute = minPartitionScore
