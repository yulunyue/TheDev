class Solution:
    """
    给定一个数组nums和一个长度为m的操作序列q
    q[i]=l,r,k,v
    for l,r,k,v in q:
      for j in range(l,r,k):
        nums[j]*=v
    求nums的异或和
    """
    def xorAfterQueries(self, nums: List[int], queries: List[List[int]]) -> int:
        "nums = [2,3,1,5,4], queries = [[1,4,2,3],[0,2,1,2]]

输出： 31"
