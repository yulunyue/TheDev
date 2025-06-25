from typing import List
from common.util.export import logger, functools, C, math, heapq
from common.algo.base.graph import Graph


class Solution:
    def get_cases(self):
        return [dict(n=3, k=2, m=3, time=[2, 5, 8], mul=[1.0, 1.5, 0.75], result=14.5)]

    def minTime(
        self, n: int, k: int, m: int, time: List[int], mul: List[float]
    ) -> float:
        h = []
