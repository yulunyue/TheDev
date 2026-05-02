from common.util.export import List, MockCf


class Solution(MockCf):
    """
    给定一个长度为n的数组nums，和一个querys么（l，r，k）数组，对于每一个nums[l，r+1]
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
            rv, rt = nums[r]
            if k < lv:
                d = k * 2
            elif k > rv:
                d = (k + rt - nums[l - 1][1]) * 2
            else:
                for i in range(l, r + 1):
                    pass
            ans.append(d)
        return ans

    execute = kthRemainingInteger
