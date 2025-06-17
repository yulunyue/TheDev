from common.util.export import List


class Solution:
    def get_cases(self):
        return [dict(nums=[3, 12, 45], k=5, result=[3, 12, 45])]

    def concatenatedDivisibility(self, nums: List[int], k: int) -> List[int]:
        nums.sort(key=lambda v: str(v))
        chen = [10 ** len(str(v)) for v in nums]
