from typing import List


class Solution:
    def get_cases(self):
        """
        [5,1,5] 贪心的反例，不能从左到右一直加
        感觉需要维护一个数据结构
        """
        return [dict(nums=[5, 2, 3, 1], result=2)]

    def mininumPairRemoval(self, nums: List[int]) -> int:
        pass
