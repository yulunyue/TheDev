from common.util.export import List, MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[0, -2, -1, -3, 0, 2, -1], result=-4),
        )

    def maxSumTrionic(self, nums: List[int]) -> int:
        pass

    execute = maxSumTrionic
