from common.util.export import MockCf


class Solution(MockCf):
    """
    将一个长度为为n的正整数数组A，恰好分成连续的k个子数组，如何求k个子数组和的平方的和的最小值
    """

    def get_cases(self):
        return dict(
            case0=dict(nums=[1, 1, 1], k=3, result=3),
            case1=dict(nums=[1, 1, 1], k=2, result=1),
        )

    def minPartitionScore(self, nums: List[int], k: int) -> int:
        pass

    execute = minPartitionScore
