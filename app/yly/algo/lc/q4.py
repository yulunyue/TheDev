from typing import List
import heapq
import math
class Solution:
    def minStable(self, nums: List[int], maxC: int) -> int:
        s=[]
        n = len(nums)
        ct=1
        for i in range(1,n):
            if math.gcd(nums[i-1],nums[i])>=2:
                ct+=1
            else:
                s.append(-ct)
                ct=1
                
        
        