from common.util.export import MockCf, List


class Solution(MockCf):
    def get_cases(self):
        return dict(case0=dict(nums=[5, 4, 5, 6], k=2, result=7))

    def maxXor(self, nums: list[int], k: int) -> int:
        pass

    execute = maxXor
