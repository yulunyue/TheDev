from typing import List
class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        
        nums=sorted([str(v)+str(v)[-1] for v in nums],reverse=True)
        return "".join([v[:-1] for v in nums])