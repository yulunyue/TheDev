from common.util.export import List, MockCf, functools


class Solution(MockCf):
    def get_cases(self):
        return dict(case0=dict(nums=[1, 3, 2, 6, 4, 2], k=3, dist=3, result=5))

    def minimumCost(self, nums: List[int], k: int, dist: int) -> int:
        pass

    execute = minimumCost
