from common.util.export import List, MockCf


class Solution(MockCf):
    """
    给定一个长度为n的数组nums
    一个querys么（l，r，k）数组，
    对于每一个q=nums[l，r+1]
    我们需要找到第大的偶数，这个偶数不在q中
    """

    def get_cases(self):
        return dict(
            case0=dict(
                nums=[1, 4, 7],
                queries=[[0, 2, 1], [1, 1, 2], [0, 0, 3]],
                expected=[2, 6, 6],
            )
        )

    def kthRemainingInteger(
        self, nums: list[int], queries: list[list[int]]
    ) -> list[int]:
        n = len(nums)
        lv = 0
        ct = 0
        for i, v in enumerate(nums):
            if v % 2 == 0:
                lv = v // 2
                ct += 1
            nums[i] = [lv, ct]
        ans = []
        for l, r, k in queries:
            lv, _ = nums[l]
            lt=0 if l==0 else nums[l-1][1]
            rv, rt = nums[r]
            if k < lv:
                d = k
            elif k > rv:
                d = k + rt -lt
            else:
                d=0
                for i in range(l, r + 1):
                    cv,ct=nums[i]
                    if ct-lt==k-lv:
                        d=ct-lt
            ans.append(d*2)
        return ans

    execute = kthRemainingInteger
