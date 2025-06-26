from common.util.export import SortedList, List


class Solution:
    def get_cases(self):
        """
        [5,1,5] 贪心的反例，不能从左到右一直加
        感觉需要维护一个数据结构
        """
        return [dict(nums=[5, 2, 3, 1], result=2)]

    def minimumPairRemoval(self, nums: List[int]) -> int:
        sl = SortedList()
        dec = 0
        n = len(nums)
        for i in range(n - 1):
            dec += nums[i] > nums[i + 1]
            sl.add([nums[i] + nums[i + 1], i])
        idx = SortedList(range(n))
        while dec:
            s, i = sl.pop(0)
            k = idx.bisect_left(i)
            ni = idx[k + 1]
            if nums[i] > nums[ni]:
                dec -= 1
            if k > 0:
                pi = idx[k - 1]
                if nums[i] < nums[pi] <= s:
                    dec -= 1
                sl.remove([nums[pi] + nums[i], pi])
                sl.add([nums[pi] + s, pi])
            if i >= 1:
                l = nums[i - 1]
            nums[i] = s
            idx.remove(ni)
