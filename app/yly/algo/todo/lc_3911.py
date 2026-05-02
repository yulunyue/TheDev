class Solution:
    """
    给定一个长度为n的数组nums，和一个querys么（l，r，k）数组，对于每一个nums[l，r+1]
    """
    def kthRemainingInteger(self, nums: list[int], queries: list[list[int]]) -> list[int]:
        nums = [1,4,7], queries = [[0,2,1],[1,1,2],[0,0,3]]

输出： [2,6,6]
      n=len(nums)
      lv=0
      ct=0
      for i,v in enumerate(nums):
          if v%2==0:
              lv=v//2
              ct+=1
          nums[i]=[lv,ct]
          


