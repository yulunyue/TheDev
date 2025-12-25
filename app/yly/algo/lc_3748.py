"""
给定一个数组 nums
查询数组q
要求对于q中的每一个l,r
nums[l,r+1]中有效子数组(任意两个相邻元素非递减)的数量



"""
class Solution:
    def countStableSubarrays(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        
